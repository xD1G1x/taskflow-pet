from django.db.models import Q
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter

from .models import Task, Comment
from .serializers import TaskSerializer, CommentSerializer
from apps.common.permissions import IsProjectOwnerOrAssigneeReadOnly, IsAuthorOrReadOnly


class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated, IsProjectOwnerOrAssigneeReadOnly]
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_fields = ["status", "priority", "project"]
    search_fields = ["title", "description"] 
    ordering_fields = ["due_date", "created_at", "priority", "status"]
    ordering = ["-created_at"]

    def get_queryset(self): # type: ignore[override]
        user = self.request.user
        return Task.objects.filter(
            Q(project__owner=user) | Q(assignees=user)
        ).distinct()


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, IsAuthorOrReadOnly]
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_fields = ["task", "author"]
    search_fields = ["text"]
    ordering_fields = ["created_at"]
    ordering = ["created_at"]

    def get_queryset(self): # type: ignore[override]
        user = self.request.user
        return Comment.objects.filter(
            Q(task__project__owner=user) | Q(task__assignees=user)
        ).distinct()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
