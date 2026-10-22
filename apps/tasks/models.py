from django.db import models
from apps.projects.models import Project
from django.conf import settings

# Create your models here.

class Status(models.TextChoices):
    TODO = "todo", "To do"
    IN_PROGRESS = "in_progress", "In Progress"
    DONE = "done", "Done"
    
class Priority(models.TextChoices):
    LOW = "low", "Low"
    MEDIUM = "medium", "Medium"
    HIGH = "high", "High"
    
class Task(models.Model):
    title = models.CharField(max_length=150)
    description = models.TextField(blank=True, default="")
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.TODO, db_index=True)
    priority = models.CharField(max_length= 20, choices=Priority.choices, default=Priority.MEDIUM, db_index=True)
    due_date = models.DateField(null=True, blank=True, db_index=True)
    project = models.ForeignKey(Project, on_delete= models.CASCADE, related_name="tasks")
    assignees = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="assigned_tasks", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self) -> str:
        return self.title
    
    class Meta:
        ordering = ["-created_at"]
        indexes = [models.Index(fields=["status", "due_date"])]
    
class Comment(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, related_name="comments", null= True, blank=True)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self) -> str:
        return self.text
    