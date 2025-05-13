from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Doctor, VerifiedDoctorRegistry, Patient

admin.site.register(Doctor)
admin.site.register(VerifiedDoctorRegistry)
admin.site.register(Patient)
