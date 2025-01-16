import re
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required

from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from api_management.serializers import UserSerializer

#api endpoint for User model
class UserAPI(APIView):
    # Get all users or a specific user by ID
    def get(self, request, pk=None):
        if pk:
            try:
                user = User.objects.get(pk=pk)
                serializer = UserSerializer(user)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except User.DoesNotExist:
                return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        else:
            users = User.objects.all()
            serializer = UserSerializer(users, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

    # Create a new user
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Update an existing user
    def put(self, request, pk):
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Delete a user
    def delete(self, request, pk):
        try:
            user = User.objects.get(pk=pk)
            user.delete()
            return Response({"message": "User deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)






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

@login_required
def success_page(request):
    user_role = request.user.role
    return render(request, 'success.html', {'role': user_role})

def logout_view(request):
    logout(request)  # Use Django's logout function
    messages.success(request, "You have logged out successfully!")
    return redirect('login')
