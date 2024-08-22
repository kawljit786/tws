from django.urls import path
from . import views

urlpatterns = [
    # Home redirects to the registration page
    path('', views.register, name='home'),  # Home page set to the register view
    
    # Authentication
    path('register/', views.register, name='register'),  # You can keep this for direct access to register
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # Task Management
    path('tasks/', views.task_list, name='task-list'),  # List all tasks
    path('tasks/create/', views.task_create, name='task-create'),  # Create a new task
    path('tasks/<int:task_id>/', views.task_detail, name='task-detail'),  # View a specific task's details
    path('tasks/<int:task_id>/update/', views.task_update, name='task-update'),  # Update an existing task
    path('tasks/<int:task_id>/delete/', views.task_delete, name='task-delete'),  # Delete a task


    path('tasks/<int:task_id>/comments/create/', views.comment_create, name='comment-create')
]
