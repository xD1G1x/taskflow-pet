import pytest
from django.db import IntegrityError
from django.db.models import ProtectedError
from django.contrib.auth import get_user_model
from datetime import date

from apps.projects.models import Project

User = get_user_model()


@pytest.mark.django_db
def test_project_str():
    user = User.objects.create_user(username="u1", password="pass")
    project = Project.objects.create(name="Demo", owner=user)
    assert str(project) == "Demo"


@pytest.mark.django_db
def test_project_unique_name_per_owner():
    user = User.objects.create_user(username="u1", password="pass")
    Project.objects.create(name="Demo", owner=user)
    with pytest.raises(IntegrityError):
        Project.objects.create(name="Demo", owner=user)


@pytest.mark.django_db
def test_project_protect_owner():
    user = User.objects.create_user(username="u1", password="pass")
    Project.objects.create(name="Demo", owner=user)
    with pytest.raises(ProtectedError):
        user.delete()