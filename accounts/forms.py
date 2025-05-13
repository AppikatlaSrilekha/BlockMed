from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.utils import timezone

from .models import User, Doctor, VerifiedDoctorRegistry, Patient
from .sm import contract, web3

class DoctorRegistrationForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data['email']
        if not VerifiedDoctorRegistry.objects.filter(email=email).exists():
            raise forms.ValidationError("Email not found in verified doctor registry.")
        return email

class DoctorProfileForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = ['specialization', 'phone', 'address']


# forms.py

class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = [
            'name', 'dob', 'phone', 'address', 'email',
            'symptoms', 'diagnosis', 'admitted',
            'date_admitted', 'date_discharged', 'doctor_incharge'
        ]
        widgets = {
            'dob': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'date_admitted': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'date_discharged': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }

    def save_to_smart_contract(self):
        patient = super().save(commit=False)
        doctor_username = str(patient.doctor_incharge.user.username) if patient.doctor_incharge else "None"
        patient.timestamp = timezone.now()  # Use timezone.now() to get the current datetime
        # Get Unix timestamp (float)

        # Prepare the input as a single dictionary representing the PatientInput struct
        patient_input = {
            'name': str(patient.name),
            'dob': str(patient.dob),  # Ensure dob is a string
            'phone': str(patient.phone),
            'addressInfo': str(patient.address),
            'email': str(patient.email),
            'symptoms': str(patient.symptoms),
            'diagnosis': str(patient.diagnosis),
            'admitted': bool(patient.admitted),
            'dateAdmitted': str(patient.date_admitted) if patient.date_admitted else "",
            'dateDischarged': str(patient.date_discharged) if patient.date_discharged else "",
            'doctorUsername': doctor_username,
            'timestamp': patient.timestamp.isoformat()  # Convert timestamp to int and then to string
        }
        tx_hash = contract.functions.saveDetails(patient_input).transact()
        web3.eth.wait_for_transaction_receipt(tx_hash)
        patient.save()
        return patient
