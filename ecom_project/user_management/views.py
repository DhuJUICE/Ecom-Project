import re
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import user

def LoginPage(request):
    return render(request, 'login.html')

def successPage(request):
    return render(request, 'success.html')

def register(request):
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

        # Check if email matches the required format
        if not re.match(email_format, email):
            messages.error(request, "Email must be in the format: name@example.com")
            return render(request, 'sign_up.html')
        
        # Check if password matches the required format
        if not re.match(password_format, password):
            messages.error(request, "Password must be at least 8 characters long, include an uppercase letter, a lowercase letter, a digit, and a special character.")
            return render(request, 'sign_up.html')

        # Check if passwords match
        if password != confirm_password:
            messages.error(request, "Passwords do not match!")
            return render(request, 'sign_up.html')
        
        # Check if email already exists
        if user.objects.filter(email_address=email).exists():
            messages.error(request, "Email already exists.")
            return render(request, 'sign_up.html')

        # Save to database
        new_user = user.objects.create(
            first_name=first_name,
            last_name=last_name,
            email_address=email
        )

        # Add your user creation logic here
        messages.success(request, "User registered successfully!")
        return redirect('success') 

    return render(request, 'sign_up.html')
