from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('register/', views.doctor_register, name='register'),
    path('login/', views.login_view, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('logout/', views.logout_view, name='logout'),
    path('toggle_verification/<int:doctor_id>/', views.toggle_verification, name='toggle_verification'),
    path('forgot_password/', views.forgot_password_view, name='forgot_password'),
    # Doctor URLs
    path('doctor/dashboard/', views.doctor_dashboard, name='doctor_dashboard'),
    path('doctor/home/', views.doctor_home, name='doctor_home'),
    path('doctor/profile/', views.doctor_profile_view, name='doctor_profile'),
    path('doctor/add_patient/', views.add_patient_view, name='add_patient'),
    # Admin URLs
    path('admin/home/', views.admin_home, name='admin_home'),
    path('admin/view_doctor/', views.admin_doctor_view, name='admin_doctor_view'),
    path('admin/view_blockchain/', views.admin_blockchain_view, name='admin_blockchain_view'),
]
