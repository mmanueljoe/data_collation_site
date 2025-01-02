from django import forms
from .models import Member, Monitor


class MemberLoginForm(forms.Form):
    agent_code = forms.CharField(max_length=100, label="Agent Code")
    password = forms.CharField(widget=forms.PasswordInput, label="Password")

    def clean(self):
        cleaned_data = super().clean()
        agent_code = cleaned_data.get('agent_code')
        password = cleaned_data.get('password')

        # Validate the agent code and password
        try:
            member = Member.objects.get(agent_code=agent_code)
            if not member.check_password(password):
                raise forms.ValidationError("Invalid agent code or password.")
        except Member.DoesNotExist:
            raise forms.ValidationError("Invalid agent code or password.")
        
        # If successful, pass the `member` object for later use
        cleaned_data['member'] = member
        return cleaned_data





class MonitorLoginForm(forms.Form):
    email = forms.EmailField(label="Email")
    password = forms.CharField(widget=forms.PasswordInput, label="Password")

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get("email")
        password = cleaned_data.get("password")

        try:
            monitor = Monitor.objects.get(email=email)
            if not monitor.check_password(password):
                raise forms.ValidationError("Invalid email or password.")
        except Monitor.DoesNotExist:
            raise forms.ValidationError("Invalid email or password.")

        cleaned_data['monitor'] = monitor
        return cleaned_data
    

class MemberDetailsForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = [
            'first_name', 'last_name', 'voter_id', 'phone_number', 'photo', 
            'address', 'occupation', 'education_background', 'birthdate', 
            'ndc_membership_status', 'agent_code', 'email'
        ]
        
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your first name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your last name'}),
            'voter_id': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your voter ID'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your phone number'}),
            'photo': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Enter your address'}),
            'occupation': forms.Select(attrs={'class': 'form-control'}),
            'education_background': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your education background'}),
            'birthdate': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'ndc_membership_status': forms.Select(choices=[('yes', 'Yes'), ('no', 'No')], attrs={'class': 'form-control'}),
            'agent_code': forms.TextInput(attrs={'readonly': 'readonly', 'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'readonly': 'readonly', 'class': 'form-control'}),
        }

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        if not phone_number.isdigit() or len(phone_number) not in [10, 12]:
            raise forms.ValidationError("Enter a valid phone number.")
        return phone_number