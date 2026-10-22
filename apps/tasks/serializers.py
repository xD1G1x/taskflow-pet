from rest_framework import serializers
from .models import Task, Comment


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = (
            "id",
            "title",
            "description",
            "status",
            "priority",
            "due_date",
            "project",
            "assignees",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("id", "created_at", "updated_at")
    
    def validate(self, attrs):
        request = self.context.get("request")
        if request and request.method == "PATCH":
            instance = self.instance
            if instance and instance.project.owner != request.user:
                if set(attrs) - {"status"}:
                    raise serializers.ValidationError (
                        "Assignee can only change task status"
                    )
        return attrs


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ("id", "task", "text", "created_at", "author")
        read_only_fields = ("id", "created_at", "author")
