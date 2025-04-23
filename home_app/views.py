from django.shortcuts import render, redirect
from .models import CustomUser, Profile
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required

@login_required
def service_provider_dashboard(request):
    return render(request, 'service_provider/service_provider_dashboard.html')

def index(request):
    return render(request, 'home_app/index.html')

def register(request):
    if request.method == "POST":
        full_name = request.POST.get("full_name")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")
        role = request.POST.get("role")  # Get selected role (customer/service_provider)

        if not (full_name and email and password and confirm_password and role):
            return render(request, "home_app/register.html", {"error": "All fields are required!"})

        if password != confirm_password:
            return render(request, "home_app/register.html", {"error": "Passwords do not match!"})

        if CustomUser.objects.filter(email=email).exists():
            return render(request, "home_app/register.html", {"error": "Email is already registered!"})

        # Create user
        user = CustomUser.objects.create_user(
            email=email, password=password, full_name=full_name,
            is_customer=(role == "customer"), is_service_provider=(role == "service_provider")
        )
        user.save()

        # Create profile with the selected role
        Profile.objects.create(user=user, role=role)

        return redirect("login")  # Redirect to login page after successful registration

    return render(request, "home_app/register.html")

def login_view(request):
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]
        user = authenticate(request, email=email, password=password)

        if user:
            login(request, user)

            if user.is_service_provider:
                return redirect("service_provider_dashboard")
            else:
                return redirect("customer_dashboard")

        return render(request, "home_app/login.html", {"error": "Invalid credentials"})

    return render(request, 'home_app/login.html')

def service_provider_login(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, email=email, password=password)
        
        if user is not None:
            profile, created = Profile.objects.get_or_create(user=user, defaults={"role": "customer"})
            
            if profile.role == "service_provider":
                login(request, user)
                return redirect('service_provider_dashboard')

        messages.error(request, "Invalid credentials or not a Service Provider")

    return render(request, 'service_provider/service_provider_login.html')
