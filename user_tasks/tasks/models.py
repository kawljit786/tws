# tasks/models.py
from django.db import models
from django.contrib.auth.models import User

class Task(models.Model):
    TODO = 'Todo'
    INPROGRESS = 'Inprogress'
    DONE = 'Done'

    STATUS_CHOICES = [
        (TODO, 'Todo'),
        (INPROGRESS, 'Inprogress'),
        (DONE, 'Done'),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField()
    due_date = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=TODO)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_tasks')
    members = models.ManyToManyField(User, related_name='tasks', blank=True)

    def __str__(self):
        return self.title

class Comment(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.user.username} on {self.task.title}'
