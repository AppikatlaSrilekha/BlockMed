from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class User(AbstractUser):
    is_doctor = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    specialization = models.CharField(max_length=100)
    phone = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)
    verified = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

class VerifiedDoctorRegistry(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)

class Patient(models.Model):
    name = models.CharField(max_length=100)
    dob = models.DateField()
    phone = models.CharField(max_length=15)
    address = models.TextField()
    email = models.EmailField()

    # New Health-Related Fields
    symptoms = models.TextField()
    diagnosis = models.TextField()
    admitted = models.BooleanField(default=False)
    date_admitted = models.DateField(null=True, blank=True)
    date_discharged = models.DateField(null=True, blank=True)
    doctor_incharge = models.ForeignKey(Doctor, on_delete=models.SET_NULL, null=True, blank=True)
    timestamp = models.DateTimeField(default=timezone.now)  # Correct usage

    def __str__(self):
        return self.name

