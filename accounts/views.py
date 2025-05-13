from django.contrib import messages
from django.contrib.auth import authenticate, login
from .forms import DoctorRegistrationForm
from .models import Doctor, Patient, User
from django.shortcuts import get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import logout
from .forms import DoctorProfileForm
from django.shortcuts import  redirect
from .forms import PatientForm
from django.contrib.auth.decorators import login_required
from .sm import contract, web3
from django.shortcuts import render

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            if user.is_doctor:
                doctor = Doctor.objects.filter(user=user).first()
                if not doctor or not doctor.verified:
                    messages.error(request, "Your account is not yet verified by admin.")
                    return render(request, 'login.html')
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid username or password.")
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('login')  # Make sure 'login' is your login page URL name

def forgot_password_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        new_password = request.POST.get('new_password')

        try:
            user = User.objects.get(username=username)
            if user.is_doctor:  # Only allow doctors to reset
                user.set_password(new_password)  # Hash the password
                user.save()
                messages.success(request, 'Password reset successful! You can now login with your new password.')
                return redirect('login')
            else:
                messages.error(request, 'Only doctors are allowed to reset password here.')
        except User.DoesNotExist:
            messages.error(request, 'Username not found.')

    return render(request, 'forgot_password.html')

def doctor_register(request):
    if request.method == 'POST':
        form = DoctorRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_doctor = True
            user.save()
            Doctor.objects.create(user=user, specialization="To be filled", verified=True)
            return redirect('login')
    else:
        form = DoctorRegistrationForm()
    return render(request, 'registration.html', {'form': form})

def dashboard(request):
    if request.user.is_superuser or request.user.is_admin:
        doctors = Doctor.objects.select_related('user').all()
        return render(request, 'admin_home.html', {'doctors': doctors})

    elif request.user.is_doctor:
        doctor = Doctor.objects.get(user=request.user)

        if request.method == 'POST':
            form = DoctorProfileForm(request.POST, instance=doctor)
            if form.is_valid():
                form.save()
        else:
            form = DoctorProfileForm(instance=doctor)

        return render(request, 'doctor_home.html', {'doctor': doctor, 'form': form})

@login_required
def doctor_home(request):
    return render(request, 'doctor_home.html')  # Simple page

# Admin views
@login_required
@staff_member_required
def admin_home(request):
    return render(request, 'admin_home.html')

@login_required
@staff_member_required
def admin_doctor_view(request):
    doctors = Doctor.objects.select_related('user').all()
    return render(request, 'admin_doctor_view.html', {'doctors': doctors})

@staff_member_required
def toggle_verification(request, doctor_id):
    doctor = get_object_or_404(Doctor, id=doctor_id)
    doctor.verified = not doctor.verified
    doctor.save()
    return redirect('dashboard')

@login_required
def admin_blockchain_view(request):
    if not request.user.is_superuser and not request.user.is_admin:
        return redirect('login')
    try:
        patients = Patient.objects.all().select_related('doctor_incharge')
        return render(request, 'admin_blockchain_view.html', {'patients': patients})
    except Exception as e:
        import traceback
        print(traceback.format_exc())
        return render(request, 'admin_blockchain_view.html', {'error': f"Error fetching patient details: {str(e)}"})

# Doctor views
@login_required
def doctor_dashboard(request):
    doctor = Doctor.objects.get(user=request.user)
    form = DoctorProfileForm(instance=doctor)
    if request.method == 'POST':
        form = DoctorProfileForm(request.POST, instance=doctor)
        if form.is_valid():
            form.save()
    return render(request, 'doctor_home.html', {'doctor': doctor, 'form': form})

@login_required
def add_patient_view(request):
    if request.method == 'POST':
        form = PatientForm(request.POST)
        if form.is_valid():
            form.save_to_smart_contract()
            messages.success(request, 'Patient added and recorded in blockchain!')
    else:
        form = PatientForm()
    return render(request, 'add_patient.html', {'patient_form': form})

@login_required
def doctor_profile_view(request):
    doctor = Doctor.objects.get(user=request.user)

    if request.method == 'POST':
        form = DoctorProfileForm(request.POST, instance=doctor)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect('doctor_profile')
    else:
        form = DoctorProfileForm(instance=doctor)

    return render(request, 'doctor_profile.html', {'form': form})

# Ensure Web3 is connected
if web3.is_connected():
    print("Connected to Ganache")
else:
    print("Failed to connect to Ganache")
#
# def sm_add_patient(request):
#     if request.method == 'POST':
#         name = request.POST['name']
#         age = int(request.POST['age'])
#         gender = request.POST['gender']
#         diagnosis = request.POST['diagnosis']
#         try:
#             tx_hash = contract.functions.saveDetails(name, age, gender, diagnosis).transact({'from': web3.eth.default_account})
#             web3.eth.wait_for_transaction_receipt(tx_hash)
#             return HttpResponse("✅ Patient added to blockchain successfully.")
#         except Exception as e:
#             return HttpResponse(f"Error adding patient: {str(e)}")
#     return render(request, 'sm_add_patient.html')
#
#
# def sm_view_patient(request):
#     if request.method == 'GET':
#         try:
#             # Fetch details for the default account set in web3.eth.default_account
#             name, age, gender, diagnosis = contract.functions.getMyDetails().call()
#             context = {
#                 'name': name,
#                 'age': age,
#                 'gender': gender,
#                 'diagnosis': diagnosis
#             }
#             return render(request, 'sm_view_patient.html', context)
#         except Exception as e:
#             import traceback
#             print(traceback.format_exc())
#             return render(request, 'sm_view_patient.html', {'error': f"Error fetching patient details: {str(e)}"})
#