# tasks/urls.py

from django.urls import path
from .views import (
    TaskCreateView, TaskListView, TaskDetailView, TaskUpdateView, TaskDeleteView,
    TaskMemberAddView, TaskMemberRemoveView, TaskMembersListView,
    CommentCreateView, TaskStatusUpdateView
)

urlpatterns = [
    path('create/', TaskCreateView.as_view(), name='task-create'),
    path('list', TaskListView.as_view(), name='task-list'),
    path('<int:pk>/', TaskDetailView.as_view(), name='task-detail'),
    path('<int:pk>/update/', TaskUpdateView.as_view(), name='task-update'),
    path('<int:pk>/delete/', TaskDeleteView.as_view(), name='task-delete'),
    path('<int:task_id>/members/', TaskMembersListView.as_view(), name='task-members'),
    path('<int:task_id>/members/add/', TaskMemberAddView.as_view(), name='task-member-add'),
    path('<int:task_id>/members/remove/<int:user_id>/', TaskMemberRemoveView.as_view(), name='task-member-remove'),
    path('<int:task_id>/comments/add/', CommentCreateView.as_view(), name='task-comment-add'),
    path('<int:pk>/status/', TaskStatusUpdateView.as_view(), name='task-status-update'),
]
