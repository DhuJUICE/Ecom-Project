import re
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
from .models import User

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Authenticate user
        user = authenticate(request, username=email, password=password)

        if user:
            login(request, user)  # Use Django's login function
            messages.success(request, "Login successful!")
            return redirect('success')  # Redirect to success page
        else:
            messages.error(request, "Invalid email or password.")
            return render(request, 'login.html', {"email": email})  # Keep entered email for convenience

    return render(request, 'login.html')

def register_view(request):
    if request.method == 'POST':
        first_name = request.POST.get('firstname')
        last_name = request.POST.get('lastname')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        # Define your password format using a regex
        password_format = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$'

        # Custom email format validation
        email_format = r'^[a-zA-Z0-9._%+-]+@gmail\.com$'

        # Validate email format
        if not re.match(email_format, email):
            messages.error(request, "Email must be in the format: name@gmail.com")
            return render(request, 'sign_up.html')

        # Validate password format
        if not re.match(password_format, password):
            messages.error(request, "Password must be at least 8 characters long, include an uppercase letter, a lowercase letter, a digit, and a special character.")
            return render(request, 'sign_up.html')

        # Check if passwords match
        if password != confirm_password:
            messages.error(request, "Passwords do not match!")
            return render(request, 'sign_up.html')

        # Check if email already exists
        if User.objects.filter(email_address=email).exists():
            messages.error(request, "Email already exists.")
            return render(request, 'sign_up.html')

        # Save to database
        new_user = User(
            first_name=first_name,
            last_name=last_name,
            email_address=email,
            password=make_password(password)  # Hash password
        )
        new_user.save()

        messages.success(request, "User registered successfully!")
        return redirect('success')

    return render(request, 'sign_up.html')

def success_page(request):
    return render(request, 'success.html')

def logout_view(request):
    logout(request)  # Use Django's logout function
    messages.success(request, "You have logged out successfully!")
    return redirect('login')
