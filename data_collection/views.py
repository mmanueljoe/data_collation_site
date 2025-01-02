from datetime import timezone, datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .forms import MonitorLoginForm, MemberLoginForm
from django.contrib.auth import get_user_model
from django.contrib import messages
from collections import Counter
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.db.models import Q
import csv
import openpyxl
import uuid
from django.contrib.auth import logout
from .forms import MonitorLoginForm
from .models import Member, Monitor
from .forms import MemberDetailsForm
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.paginator import Paginator
from collections import defaultdict
from datetime import date
from django.http import HttpResponse
from django.template.loader import render_to_string
from io import BytesIO
from xhtml2pdf import pisa
from django.http import HttpResponse
from django.template.loader import get_template
import logging
from django.http import JsonResponse
from django.shortcuts import render
from django.db.models import Q
from django.core.paginator import Paginator
from .models import Member


logger = logging.getLogger(__name__)


def member_login(request):
    if request.method == 'POST':
        form = MemberLoginForm(request.POST)
        if form.is_valid():
            # Retrieve the validated member object
            member = form.cleaned_data['member']
            
            # Log in the member
            login(request, member, backend='data_collection.auth_backends.AgentCodeBackend')
            return redirect('member_dashboard')
        else:
            # If the form is invalid, errors will already be populated
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, error)
    else:
        form = MemberLoginForm()

    return render(request, 'member_login.html', {'form': form})



def monitor_login(request):
    if request.method == 'POST':
        form = MonitorLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            try:
                monitor = Monitor.objects.get(email=email)
                if monitor.check_password(password):
                    # Explicitly set the backend
                    monitor.backend = 'data_collection.auth_backends.MonitorBackend'
                    login(request, monitor)
                    return redirect('monitor_dashboard')  # Replace with the actual dashboard URL
                else:
                    messages.error(request, 'Invalid email or password')
            except Monitor.DoesNotExist:
                messages.error(request, 'Invalid email or password')
    else:
        form = MonitorLoginForm()
    return render(request, 'monitor_login.html', {'form': form})



def generate_agent_code(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Check if email already exists
        if Member.objects.filter(email=email).exists():
            messages.error(request, "A user with this email already exists.")
            return render(request, 'generate_agent_code.html')

        # Generate a new agent code
        agent_code = Member().generate_agent_code()

        # Save the member
        member = Member.objects.create(
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password,  # Consider hashing the password before saving
            agent_code=agent_code
        )

        # Redirect to a success page or display the agent code
        return render(request, 'agent_code_generated.html', {'agent_code': agent_code, 'email': email})
    
    return render(request, 'generate_agent_code.html')



@login_required
def member_dashboard(request):
    # Ensure the authenticated user is a Member
    if not hasattr(request.user, 'agent_code'):
        return redirect('member_login')  # Redirect if the user is not a Member

    member = request.user  # Use the authenticated user directly

    # Determine time of day for greeting
    current_hour = datetime.now().hour
    if 5 <= current_hour < 12:
        greeting = "Good Morning"
    elif 12 <= current_hour < 18:
        greeting = "Good Afternoon"
    else:
        greeting = "Good Evening"

    # Handle the form submission (POST)
    if request.method == 'POST':
        form = MemberDetailsForm(request.POST, request.FILES, instance=member)
        if form.is_valid():
            form.save()  # Save the updated member details
            messages.success(request, "Your details have been successfully updated!")  # Add success message
            return redirect('member_dashboard')  # Redirect to the dashboard after saving
    else:
        form = MemberDetailsForm(instance=member)

    return render(request, 'member_dashboard.html', {
        'form': form,
        'greeting': greeting,
    })


@login_required
def monitor_dashboard(request):
    search_query = request.GET.get('search', '')
    occupation_filter = request.GET.get('occupation', '')
    ndc_filter = request.GET.get('ndc_membership_status', '')

    members = Member.objects.all()

    if search_query:
        members = members.filter(
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query) |
            Q(email__icontains=search_query) |
            Q(phone_number__icontains=search_query)
        )

    if occupation_filter:
        members = members.filter(occupation=occupation_filter)

    if ndc_filter:
        members = members.filter(ndc_membership_status=bool(int(ndc_filter)))

    paginator = Paginator(members, 10)
    page_number = request.GET.get('page')
    members_page = paginator.get_page(page_number)

    occupations = Member.objects.values_list('occupation', flat=True).distinct()

    # Get age group distribution and convert keys/values to lists
    age_distribution = get_age_distribution(members)
    age_groups = {
        'keys': list(age_distribution.keys()),
        'values': list(age_distribution.values()),
    }

    return render(request, 'monitor_dashboard.html', {
        'members': members_page,
        'occupations': occupations,
        'age_groups': age_groups,
        'ndc_count': members.filter(ndc_membership_status=True).count(),
        'non_ndc_count': members.filter(ndc_membership_status=False).count(),
    })

@login_required
def monitor_search_api(request):
    try:
        search_query = request.GET.get('search', '').strip()
        occupation_filter = request.GET.get('occupation', '').strip()
        ndc_filter = request.GET.get('ndc_membership_status', '').strip()

        members = Member.objects.all()

        if search_query:
            members = members.filter(
                Q(first_name__icontains=search_query) |
                Q(last_name__icontains=search_query) |
                Q(email__icontains=search_query) |
                Q(phone_number__icontains=search_query)
            )

        if occupation_filter:
            members = members.filter(occupation__iexact=occupation_filter)

        if ndc_filter in ('0', '1'):
            members = members.filter(ndc_membership_status=(ndc_filter == '1'))

        member_data = list(members.values(
            'id', 'first_name', 'last_name', 'phone_number', 'email', 'age', 'ndc_membership_status'
        ))
        return JsonResponse({'members': member_data})
    except Exception as e:
        print(f"Error: {e}")
        return JsonResponse({'error': 'Something went wrong.'}, status=500)



@login_required
def export_excel(request):
    members = Member.objects.all()
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.append(['First Name', 'Last Name', 'Email', 'Phone Number', 'Occupation'])  # Add headers
    for member in members:
        ws.append([member.first_name, member.last_name, member.email, member.phone_number, member.occupation])
    
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=members.xlsx'
    wb.save(response)
    return response


@login_required
def export_pdf(request):
    search_query = request.GET.get('search', '')
    occupation_filter = request.GET.get('occupation', '')
    ndc_filter = request.GET.get('ndc_membership_status', '')

    members = Member.objects.all()

    if search_query:
        members = members.filter(
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query) |
            Q(email__icontains=search_query) |
            Q(phone_number__icontains=search_query)
        )

    if occupation_filter:
        members = members.filter(occupation=occupation_filter)

    if ndc_filter:
        members = members.filter(ndc_membership_status=bool(int(ndc_filter)))

    # Use pdf_template.html here
    template = get_template('pdf_template.html')
    html = template.render({'members': members})

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="members.pdf"'

    pisa_status = pisa.CreatePDF(BytesIO(html.encode('UTF-8')), dest=response)

    if pisa_status.err:
        return HttpResponse('Error generating PDF', status=500)
    return response



@login_required
def edit_member(request, id):
    member = get_object_or_404(Member, id=id)
    
    if request.method == 'POST':
        form = MemberDetailsForm(request.POST, request.FILES, instance=member)
        if form.is_valid():
            form.save()
            messages.success(request, "Member details updated successfully")
            return redirect('monitor_dashboard')
    else:
        form = MemberDetailsForm(instance=member)
    
    return render(request, 'edit_member.html', {'form': form, 'member': member})


@login_required
def delete_member(request, id):
    # Delete member logic
    member = get_object_or_404(Member, id=id)
    if request.method == 'POST':
        member.delete()
        messages.success(request, "Member deleted successfully")
        return redirect('monitor_dashboard')
    return render(request, 'delete_member.html', {'member': member})



def member_logout(request):
    logout(request)
    return redirect('member_login')  # Redirect to the login page after logout

def monitor_logout(request):
    logout(request)
    return redirect('monitor_login')  




def get_age_distribution(members):
    age_groups = {"18-25": 0, "26-35": 0, "36-45": 0, "46-60": 0, "60+": 0}
    for member in members:
        if member.age is None:  # Skip members without a birthdate
            continue
        elif member.age < 18:
            continue
        elif member.age <= 25:
            age_groups["18-25"] += 1
        elif member.age <= 35:
            age_groups["26-35"] += 1
        elif member.age <= 45:
            age_groups["36-45"] += 1
        elif member.age <= 60:
            age_groups["46-60"] += 1
        else:
            age_groups["60+"] += 1
    return dict(Counter(age_groups))