from django.db import models
from django.contrib.auth.models import AbstractUser
from apps.projects.models import Project
from apps.tasks.models import Task, Comment

# Create your models here.


class User(AbstractUser):
    pass    
