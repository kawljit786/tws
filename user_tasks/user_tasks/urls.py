# myproject/urls.py

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('tasks/', include('tasks.urls')),     # Include tasks URLs
    path('', include('users.urls')),           # Default to users app (for register/login/logout)
]
