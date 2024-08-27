# myproject/urls.py

from django.contrib import admin
from django.urls import path, include
# from users.views import RegisterView , register
from users.views import register

# urlpatterns = [
#     path('admin/', admin.site.urls),
#     # path('register/', RegisterView.as_view(), name='register'),
#     path('users/', include('users.urls')),
#     path('tasks/', include('tasks.urls')), 
#     path('', RegisterView.as_view(), name='home'),  # Default route
# ]


urlpatterns = [
    path('admin/', admin.site.urls),
    # path('register/', include('users.urls')),  # User-related URLs
    path('tasks/', include('tasks.urls')),     # Include tasks URLs
    path('', include('users.urls')),           # Default to users app (for register/login/logout)
    path('', register, name='home'),  # Default route
]
