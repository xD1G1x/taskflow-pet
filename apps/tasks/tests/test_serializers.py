import pytest
from datetime import date, timedelta
from apps.tasks.serializers import TaskSerializer
from apps.projects.models import Project
from apps.tasks.models import Task
from django.contrib.auth import get_user_model
from rest_framework.test import APIRequestFactory

User = get_user_model()


@pytest.mark.django_db
def test_task_serializer_valid():
    user = User.objects.create_user(username="u1", password="pass")
    project = Project.objects.create(name="Demo", owner=user)
    data = {"title": "T", "project": project.id, "status": "todo"}
    s = TaskSerializer(data=data)
    assert s.is_valid(), s.errors


@pytest.mark.django_db
def test_task_serializer_invalid_status():
    user = User.objects.create_user(username="u1", password="pass")
    project = Project.objects.create(name="Demo", owner=user)
    data = {"title": "T", "project": project.id, "status": "wrong"}
    s = TaskSerializer(data=data)
    assert not s.is_valid()
    assert "status" in s.errors


@pytest.mark.django_db
def test_task_serializer_due_date_in_past():
    user = User.objects.create_user(username="u1", password="pass")
    project = Project.objects.create(name="Demo", owner=user)
    data = {
        "title": "T", "project": project.id,
        "due_date": (date.today() - timedelta(days=1)).isoformat(),
    }
    s = TaskSerializer(data=data)
    assert not s.is_valid()
    assert "due_date" in s.errors
    
@pytest.mark.django_db
def test_task_serializer_validate_assignee_change_title():
    owner = User.objects.create_user(username="u1", password="pass")
    project = Project.objects.create(name="Demo", owner=owner)
    assignee = User.objects.create_user(username="a1", password="pass")
    task = Task.objects.create(title = "Demo_task", project = project, status = "todo" )
    task.assignees.add(assignee)
    request = APIRequestFactory().patch(
        "/tasks/1/",
        {"title": "New title"},
        format="json"
    )
    request.user = assignee

    s = TaskSerializer(
        task,
        data={"title": "New title"},
        partial=True,
        context={"request": request}
    )

    assert not s.is_valid(), "non_field_errors" in s.errors 
    
@pytest.mark.django_db
def test_task_serializer_validate_assignee_change_status():
    owner = User.objects.create_user(username="u1", password="pass")
    project = Project.objects.create(name="Demo", owner=owner)
    assignee = User.objects.create_user(username="a1", password="pass")
    task = Task.objects.create(title = "Demo_task", project = project, status = "todo" )
    task.assignees.add(assignee)
    request = APIRequestFactory().patch(
        "/tasks/1/",
        {"status": "done"},
        format="json"
    )
    request.user = assignee

    s = TaskSerializer(
        task,
        data={"status": "done"},
        partial=True,
        context={"request": request}
    )

    assert s.is_valid(), s.errors