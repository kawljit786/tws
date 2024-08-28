from django.urls import path
from users.views import LoginView, RegisterView, logout_view


urlpatterns = [
    path('', RegisterView.as_view(), name='home'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', logout_view, name='logout'),
]