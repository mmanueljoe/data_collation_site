from django.contrib import admin
from django import forms
from .models import Member, Monitor

# Custom form for updating Member passwords
class MemberChangeForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput,
        required=False,
        help_text="Leave empty if you don't want to change the password.",
    )

    class Meta:
        model = Member
        fields = '__all__'

    def save(self, commit=True):
        member = super().save(commit=False)
        password = self.cleaned_data.get('password')
        if password:
            member.password = password  # Save plain text temporarily
            member.set_password(password)  # Hash the password
        if commit:
            member.save()
        return member

@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    form = MemberChangeForm
    list_display = ('agent_code', 'first_name', 'last_name', 'ndc_membership_status')
    search_fields = ('agent_code', 'first_name', 'last_name')

# Custom form for updating Monitor passwords
class MonitorChangeForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput,
        required=False,
        help_text="Leave empty if you don't want to change the password.",
    )

    class Meta:
        model = Monitor
        fields = '__all__'

    def save(self, commit=True):
        monitor = super().save(commit=False)
        password = self.cleaned_data.get('password')
        if password:
            monitor.password = password  # Save plain text temporarily
            monitor.set_password(password)  # Hash the password
        if commit:
            monitor.save()
        return monitor

@admin.register(Monitor)
class MonitorAdmin(admin.ModelAdmin):
    form = MonitorChangeForm
    list_display = ('email', 'first_name', 'last_name')
    search_fields = ('email', 'first_name', 'last_name')
