from django.shortcuts import render
from django.contrib import messages
import re

def LoginPage(request):
    return render(request, 'login.html')

def SignUpPage(request):
    return render(request, 'sign_up.html')

def register(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        
         # Define your password format using a regex
        password_format = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$'

        # Custom email format validation
        email_format = r'^[a-zA-Z0-9._%+-]+@example\.com$'

        # Check if email matches the required format
        if not re.match(email_format, email):
            messages.error(request, "Email must be in the format: name@example.com")
            return render(request, 'sign_up.html', {'error': "Invalid email format!"})
        
        # Check if password matches the required format
        if not re.match(password_format, password):
            messages.error(request, "Password must be at least 8 characters long, include an uppercase letter, a lowercase letter, a digit, and a special character.")
            return render(request, 'sign_up.html', {'error': "Invalid password format!"})

        # Check if passwords match
        if password != confirm_password:
            messages.error(request, "Passwords do not match!")
            return render(request, 'sign_up.html', {'error': "Passwords do not match!"})

        # If passwords match, process the form data (e.g., save the user)
        # Add your user creation logic here
        messages.success(request, "Registration successful!")
        return render(request, 'success.html')

    return render(request, 'sign_up.html')
