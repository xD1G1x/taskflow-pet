import pytest
from django.contrib.auth import get_user_model

from apps.projects.models import Project
from apps.tasks.models import Task,Comment

User = get_user_model()

@pytest.fixture
def user1(db):
    return User.objects.create_user(username="u1", password="pass")

@pytest.fixture
def project1(db, user1):
    return Project.objects.create(name="p1", owner = user1)
