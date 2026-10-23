import pytest
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from apps.projects.models import Project

User = get_user_model()


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def user1(db):
    return User.objects.create_user(username="u1", password="pass")


@pytest.fixture
def user2(db):
    return User.objects.create_user(username="u2", password="pass")


@pytest.mark.django_db
def test_list_projects_anonymous(api_client):
    response = api_client.get("/api/projects/")
    assert response.status_code == 401


@pytest.mark.django_db
def test_list_projects_authenticated(api_client, user1):
    Project.objects.create(name="P1", owner=user1)
    api_client.force_authenticate(user=user1)
    response = api_client.get("/api/projects/")
    assert response.status_code == 200
    assert response.data["count"] == 1


@pytest.mark.django_db
def test_other_user_cannot_see_project(api_client, user1, user2):
    p = Project.objects.create(name="P1", owner=user1)
    api_client.force_authenticate(user=user2)
    response = api_client.get(f"/api/projects/{p.id}/")
    assert response.status_code == 404


@pytest.mark.django_db
def test_create_project_sets_owner(api_client, user1):
    api_client.force_authenticate(user=user1)
    response = api_client.post("/api/projects/", {"name": "New"})
    assert response.status_code == 201
    assert response.data["owner"] == user1.id
    
@pytest.mark.django_db
def test_other_user_cannot_put_project(api_client, user1, user2):
    p = Project.objects.create(name="P1", owner=user1)
    api_client.force_authenticate(user=user2)
    response = api_client.put(f"/api/projects/{p.id}/", data={"name": "P2",}, format= "json")
    assert response.status_code == 404
    
@pytest.mark.django_db
def test_delete_own_project(api_client, user1):
    p = Project.objects.create(name="P1", owner=user1)
    api_client.force_authenticate(user=user1)
    response = api_client.delete(f"/api/projects/{p.id}/")
    assert response.status_code == 204