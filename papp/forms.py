from django import forms
from .models import dr_register, Appointment,Employee_register

class DoctorRegisterForm(forms.ModelForm):
    class Meta:
        model = dr_register
        fields = ['name', 'image', 'address', 'qualifications' ,'identity_card', 'contact_no', 'email', 'password']

class EmployeeRegisterForm(forms.ModelForm):
    class Meta:
        model = Employee_register
        fields = ['name', 'image', 'address', 'qualifications', 'identity_card','contact_no', 'email', 'password']


class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['type', 'name', 'age', 'date', 'doctor']
