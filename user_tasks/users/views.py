# users/views.py

from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny


class RegisterView(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        # Render the registration form
        return render(request, 'users/register.html')

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        email = request.data.get('email')

        if User.objects.filter(username=username).exists():
            return render(request, 'users/register.html', {'error': 'Username already taken'})

        user = User.objects.create_user(username=username, password=password, email=email)
        user.save()

        # Automatically log the user in after registration
        user = authenticate(request, username=username, password=password)
        login(request, user)

        # Generate JWT tokens
        response = redirect('login')
        refresh = RefreshToken.for_user(user)
        response.set_cookie('access_token', str(refresh.access_token), httponly=True)
        response.set_cookie('refresh_token', str(refresh), httponly=True)
        return response


class LoginView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        # Render the login form
        return render(request, 'users/login.html')

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            # Generate JWT tokens
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            refresh_token = str(refresh)

            # Redirect to the task creation view after successful login
            response = redirect('task-create')

            # # Add the JWT token to the response headers for use in APIs
            response.set_cookie('refresh_token', refresh_token, httponly=True, secure=True)
            response.set_cookie('access_token', access_token, httponly=True, secure=True)
            return response
        else:
            # Invalid credentials, re-render the login page with an error message
            return render(request, 'users/login.html', {'error': 'Invalid credentials'})

def logout_view(request):
    logout(request)
    
    # Redirect to the login page
    response = redirect('login')
    
    # Clear the JWT token from cookies
    response.delete_cookie('access_token')
    
    return response
