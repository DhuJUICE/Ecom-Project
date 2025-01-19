import re
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required

from django.contrib.auth.models import User, auth
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from api_management.serializers import UserSerializer
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator


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

#function to display the login screen
def displayLogin(request):
    return render(request, 'login.html')

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Authenticate user
        user = authenticate(request, username=email, password=password)

        if user:
            login(request, user)  # Use Django's login function
            return JsonResponse({"message": "Login successful!", "status": "success"}, status=200)
        else:
            return JsonResponse({"message": "Invalid email or password.", "status": "error"}, status=401)
    else:
        return JsonResponse({"message": "Invalid request method. POST required.", "status": "error"}, status=405)

#function to display the login screen
def displayRegister(request):
    return render(request, 'sign_up.html')

def register_view(request):
    if request.method == 'POST':
        first_name = request.POST.get('firstname')
        last_name = request.POST.get('lastname')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        # Check if email already exists
        if User.objects.filter(email=email).exists():
            return JsonResponse(
                {"message": "Email already exists.", "status": "error"}, 
                status=400
            )

        # Create and save the new user
        new_user = User(
            first_name=first_name,
            last_name=last_name,
            username=email,  # Use email as the username
            email=email,
            password=make_password(password)  # Hash password for security
        )
        new_user.save()

        return JsonResponse(
            {"message": "User registered successfully!", "status": "success"}, 
            status=201
        )

    return JsonResponse(
        {"message": "Invalid request method. POST required.", "status": "error"}, 
        status=405
    )

def logout_view(request):
    auth.logout(request)
    return JsonResponse({"message": "You have logged out successfully!", "status": "success"}, status=200)