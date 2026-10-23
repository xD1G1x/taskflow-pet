import pytest
from django.contrib.auth import get_user_model
from datetime import date
from django.core.exceptions import ValidationError

from apps.projects.models import Project
from apps.tasks.models import Task,Comment

User = get_user_model()

@pytest.fixture
def user1(db):
    return User.objects.create_user(username="u1", password="pass")

@pytest.fixture
def project1(db, user1):
    return Project.objects.create(name="p1", owner = user1)

@pytest.mark.django_db
def test_task_str(project1):
    task = Task.objects.create(title="task", project = project1)
    assert str(task) == "task"
    
@pytest.mark.django_db
def test_comment_str(project1, user1):

    task = Task.objects.create(title="task", project = project1)
    comment = Comment.objects.create(task = task, author = user1, text = "comm")
    assert str(comment) == "comm"