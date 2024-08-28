from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from .models import Task, Comment
from .serializers import TaskSerializer
from django.contrib.auth.models import User
from rest_framework_simplejwt.authentication import JWTAuthentication

class TaskCreateView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request, *args, **kwargs):
        users = User.objects.all()  # Retrieve all users for member selection
        return render(request, 'tasks/task_create.html', {'users': users})

    def post(self, request, *args, **kwargs):
        data = {
            'title': request.POST.get('title'),
            'description': request.POST.get('description'),
            'due_date': request.POST.get('due_date'),
            'status': request.POST.get('status'),
            'created_by': request.user.id  # Assign the current logged-in user
        }

        serializer = TaskSerializer(data=data)
        if serializer.is_valid():
            task = serializer.save()

            # Handling members assignment
            members_ids = request.POST.getlist('members')
            members = User.objects.filter(id__in=members_ids)
            task.members.set(members)
            task.save()
            
            return redirect(reverse('task-list'))  # Redirect to the task list view

        # If the serializer is not valid, render the form with errors
        users = User.objects.all()  # Retrieve users again in case of error
        return render(request, 'tasks/task_create.html', {'errors': serializer.errors, 'users': users})



class TaskListView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request, *args, **kwargs):
        tasks = Task.objects.all()
        return render(request, 'tasks/task_list.html', {'tasks': tasks})

class TaskDetailView(APIView):
    # permission_classes = [IsAuthenticated]
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request, *args, **kwargs):
        task = get_object_or_404(Task, pk=kwargs['pk'])
        comments = Comment.objects.filter(task=task)
        return render(request, 'tasks/task_detail.html', {'task': task, 'comments': comments,  })

class TaskUpdateView(APIView):
    # permission_classes = [IsAuthenticated]
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request, *args, **kwargs):
        task = get_object_or_404(Task, pk=kwargs['pk'])
        users = User.objects.all()

        return render(request, 'tasks/task_update.html', {'task': task, 'users': users})

    def post(self, request, *args, **kwargs):
        task = get_object_or_404(Task, pk=kwargs['pk'])
        data = {
            'title': request.POST.get('title'),
            'description': request.POST.get('description'),
            'due_date': request.POST.get('due_date'),
        }
        serializer = TaskSerializer(task, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return redirect(reverse('task-detail', args=[task.pk]))
        return render(request, 'tasks/task_update.html', {'task': task, 'errors': serializer.errors})

class TaskDeleteView(APIView):
    # permission_classes = [IsAuthenticated]
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    
    def post(self, request, *args, **kwargs):
        task = get_object_or_404(Task, pk=kwargs['pk'])
        task.delete()
        return redirect(reverse('task-list'))

class TaskMemberAddView(APIView):
    # permission_classes = [IsAuthenticated]
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def post(self, request, *args, **kwargs):
        task = get_object_or_404(Task, pk=kwargs['task_id'])
        user_id = request.POST.get('user_id')
        user = get_object_or_404(User, pk=user_id)
        Task.objects.create(task=task, user=user)
        return redirect(reverse('task-detail', args=[task.pk]))

class TaskMemberRemoveView(APIView):
    # permission_classes = [IsAuthenticated]
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def post(self, request, *args, **kwargs):
        task = get_object_or_404(Task, pk=kwargs['task_id'])
        user = get_object_or_404(User, pk=kwargs['user_id'])
        Task.objects.filter(task=task, user=user).delete()
        return redirect(reverse('task-detail', args=[task.pk]))

class TaskMembersListView(APIView):
    # permission_classes = [IsAuthenticated]
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request, *args, **kwargs):
        task = get_object_or_404(Task, pk=kwargs['task_id'])
        members = Task.objects.filter(task=task)
        return render(request, 'tasks/task_members_list.html', {'task': task, 'members': members})

class CommentCreateView(APIView):
    # permission_classes = [IsAuthenticated]
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def post(self, request, *args, **kwargs):
        task = get_object_or_404(Task, pk=kwargs['task_id'])
        comment_text = request.POST.get('comment')
        Comment.objects.create(task=task, author=request.user, text=comment_text)
        return redirect(reverse('task-detail', args=[task.pk]))

class TaskStatusUpdateView(APIView):
    # permission_classes = [IsAuthenticated]
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def post(self, request, *args, **kwargs):
        task = get_object_or_404(Task, pk=kwargs['pk'])
        status = request.POST.get('status')
        if status in ['Todo', 'Inprogress', 'Done']:
            task.status = status
            task.save()
        return redirect(reverse('task-detail', args=[task.pk]))
