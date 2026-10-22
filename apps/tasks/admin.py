from django.contrib import admin
from apps.tasks.models import Task, Comment

from django.http import HttpRequest
from django.db.models.query import QuerySet
from django.db.models import Count

# Register your models here.


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("title", "project", "status", "priority", "assignees_count")
    date_hierarchy = "due_date"
    list_filter = ("status", "priority", "due_date")
    search_fields = ("title", "project__name")
    filter_horizontal = ("assignees",)
    list_select_related = ("project",)
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.annotate(_assignees_count=Count("assignees"))
    
    @admin.display(description="Assignees", ordering="_assignees_count")
    def assignees_count(self, obj):
        return obj._assignees_count


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("task", "author", "created_at")
    search_fields = ("text", "author__username")
    list_filter = ("created_at",)
    list_select_related = ("task", "author")
