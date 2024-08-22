from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.contrib.auth import login, authenticate
from django.contrib import messages
from .models import Task, Comment

# Registration View
def register(request):
    print("=====",request.method)
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        
        if password == confirm_password:
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username already exists.')
            elif User.objects.filter(email=email).exists():
                messages.error(request, 'Email is already registered.')
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()
                login(request, user)
                return redirect('home')
        else:
            messages.error(request, 'Passwords do not match.')
    
    return render(request, 'tasks/register.html')

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
    
    return render(request, 'tasks/login.html')


def logout_view(request):
    logout(request)
    return redirect('login') 
# Task List View
def task_list(request):
    tasks = Task.objects.filter(owner=request.user)
    return render(request, 'tasks/task_list.html', {'tasks': tasks})

# Task Detail View
def task_detail(request, task_id):
    task = get_object_or_404(Task, id=task_id, owner=request.user)
    comments = Comment.objects.filter(task=task)
    
    if request.method == 'POST':
        content = request.POST['content']
        comment = Comment.objects.create(task=task, user=request.user, content=content)
        comment.save()
        return redirect('task-detail', task_id=task_id)
    
    return render(request, 'tasks/task_detail.html', {'task': task, 'comments': comments})

# Task Creation View
def task_create(request):
    if request.method == 'POST':
        title = request.POST['title']
        description = request.POST['description']
        due_date = request.POST['due_date']
        status = request.POST['status']
        
        task = Task.objects.create(title=title, description=description, due_date=due_date, status=status, owner=request.user)
        task.save()
        return redirect('task-list')
    
    return render(request, 'tasks/task_form.html')

# Task Update View
def task_update(request, task_id):
    task = get_object_or_404(Task, id=task_id, owner=request.user)
    
    if request.method == 'POST':
        task.title = request.POST['title']
        task.description = request.POST['description']
        task.due_date = request.POST['due_date']
        task.status = request.POST['status']
        task.save()
        return redirect('task-list')
    
    return render(request, 'tasks/task_form.html', {'task': task})

# Task Delete View
def task_delete(request, task_id):
    task = get_object_or_404(Task, id=task_id, owner=request.user)
    
    if request.method == 'POST':
        task.delete()
        return redirect('task-list')
    
    return redirect('task-detail', task_id=task.id)


def comment_create(request, task_id):
    task = get_object_or_404(Task, id=task_id, owner=request.user)
    
    if request.method == 'POST':
        content = request.POST['content']
        if content:
            Comment.objects.create(task=task, user=request.user, content=content)
            return redirect('task-detail', task_id=task_id)
        else:
            messages.error(request, 'Comment cannot be empty.')
    
    return redirect('tasks/task-detail', task_id=task_id)