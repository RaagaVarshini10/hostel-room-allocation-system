from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import StudentProfile
def home(request):
    return render(request, "home.html")


def register(request):

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")
        full_name = request.POST.get("full_name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        register_number = request.POST.get("register_number")
        department = request.POST.get("department")
        year = request.POST.get("year")

        # Check required fields
        if not all([
            username,
            password,
            full_name,
            email,
            phone,
            register_number,
            department,
            year
        ]):
            messages.error(
                request,
                "Please fill in all fields."
            )
            return redirect("register")

        # Check username
        if User.objects.filter(username=username).exists():
            messages.error(
                request,
                "Username already exists."
            )
            return redirect("register")

        # Check register number
        if StudentProfile.objects.filter(
            register_number=register_number
        ).exists():

            messages.error(
                request,
                "Register number already exists."
            )
            return redirect("register")

        # Split full name
        name_parts = full_name.strip().split(" ", 1)

        first_name = name_parts[0]
        last_name = name_parts[1] if len(name_parts) > 1 else ""

        # Create User
        user = User.objects.create_user(
            username=username,
            password=password,
            email=email,
            first_name=first_name,
            last_name=last_name
        )

        # Create Student Profile
        StudentProfile.objects.create(
            user=user,
            phone=phone,
            register_number=register_number,
            department=department,
            year=year
        )

        messages.success(
            request,
            "Registration successful. Please login."
        )

        return redirect("login")

    return render(request, "register.html")


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)

            # Admin / Staff user
            if user.is_staff:
                return redirect("admin_dashboard")

            # Normal student
            return redirect("dashboard")

        messages.error(
            request,
            "Invalid username or password."
        )

    return render(request, "login.html")


def logout_view(request):
    logout(request)
    return redirect("home")


def dashboard(request):
    if not request.user.is_authenticated:
        return redirect("login")

    return render(request, "dashboard.html")
@login_required
def profile(request):
    return render(request, "profile.html")