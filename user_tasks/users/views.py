# users/views.py

# from django.shortcuts import render, redirect, reverse
# from django.contrib.auth import authenticate
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework.authtoken.models import Token
# from rest_framework.permissions import IsAuthenticated, AllowAny
# from .serializers import UserSerializer
# from django.contrib.auth import authenticate, login

# class RegisterView(APIView):
#     permission_classes = [AllowAny]
#     def get(self, request):
#         return render(request, 'register.html')

#     def post(self, request):
#         data = {
#             'username': request.POST.get('username'),
#             'email': request.POST.get('email'),
#             'password': request.POST.get('password')
#         }
#         serializer = UserSerializer(data=data)
#         if serializer.is_valid():
#             user = serializer.save()
#             token, created = Token.objects.get_or_create(user=user)
#             response = redirect('login')  # Redirect to login after successful registration
#             response.set_cookie(key='auth_token', value=token.key, httponly=True)
#             return response
#         else:
#             return render(request, 'register.html', {'errors': serializer.errors})


# class LoginView(APIView):
#     permission_classes = [AllowAny]

#     def get(self, request, *args, **kwargs):
#         return render(request, 'login.html')

#     def post(self, request, *args, **kwargs):
#         username = request.POST.get('username')
#         password = request.POST.get('password')
#         user = authenticate(username=username, password=password)
#         if user is not None:
#             login(request, user)
#             return redirect(reverse('task-list'))
#         return render(request, 'login.html', {'error': 'Invalid credentials'})

# # class LoginView(APIView):
# #     permission_classes = [AllowAny]
# #     def get(self, request):
# #         return render(request, 'login.html')

# #     def post(self, request):
# #         username = request.data.get('username')
# #         password = request.data.get('password')
# #         user = authenticate(username=username, password=password)
# #         if user:
# #             token, created = Token.objects.get_or_create(user=user)
# #             response = Response({"token": token.key})
# #             response.set_cookie(key='auth_token', value=token.key, httponly=True)
# #             return redirect('/tasks/create/')  # Redirect to the task creation page
# #         return Response({"error": "Invalid credentials"}, status=400)

# class LogoutView(APIView):
#     permission_classes = [IsAuthenticated]

#     def get(self, request):
#         return render(request, 'logout.html')

#     def post(self, request):
#         request.user.auth_token.delete()
#         response = Response({"message": "Logged out successfully"})
#         response.delete_cookie('auth_token')
#         return response


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.contrib.auth import login, authenticate
from django.contrib import messages
# from .models import Task, Comment

# Registration View
def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        
        if password:
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username already exists.')
            elif User.objects.filter(email=email).exists():
                messages.error(request, 'Email is already registered.')
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()
                # login(request, user)
                return redirect('login')
        else:
            messages.error(request, 'Passwords do not match.')
    
    return render(request, 'register.html')

# Login View
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('task-create')
        else:
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    return redirect('login') 