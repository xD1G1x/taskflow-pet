from django.db.models import Q
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import Task, Comment
from .serializers import TaskSerializer, CommentSerializer
from apps.common.permissions import IsProjectOwnerOrAssigneeReadOnly, IsAuthorOrReadOnly


class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated, IsProjectOwnerOrAssigneeReadOnly]

    def get_queryset(self): # type: ignore[override]
        user = self.request.user
        return Task.objects.filter(
            Q(project__owner=user) | Q(assignees=user)
        ).distinct()


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, IsAuthorOrReadOnly]

    def get_queryset(self): # type: ignore[override]
        user = self.request.user
        return Comment.objects.filter(
            Q(task__project__owner=user) | Q(task__assignees=user)
        ).distinct()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
