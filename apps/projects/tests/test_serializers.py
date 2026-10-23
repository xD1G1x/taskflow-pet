import pytest
from django.contrib.auth import get_user_model

from apps.projects.serializers import ProjectSerializer

User = get_user_model()

@pytest.mark.django_db
def test_project_serializer_valid():
    user = User.objects.create_user(username="u1", password="pass")
    data = {"name":"N", "owner" : user.id, "description": "DESCRIPTION"}
    s = ProjectSerializer(data = data)
    assert s.is_valid(), s.errors
    assert "owner" not in s.validated_data