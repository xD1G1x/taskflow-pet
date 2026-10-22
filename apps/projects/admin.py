from django.contrib import admin
from django.db.models.query import QuerySet
from django.http import HttpRequest
from apps.projects.models import Project

from django.db.models import Count

# Register your models here.


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("name", "owner", "task_count", "created_at")
    list_filter = ("created_at", "owner")
    search_fields = ("name", "owner__username")
    readonly_fields = ("created_at", "updated_at")
    list_select_related = ("owner",)
    

    def get_queryset(self, request: HttpRequest) -> QuerySet:
        qs = super().get_queryset(request)
        return qs.annotate(_task_count=Count("tasks"))

    @admin.display(description="Tasks", ordering="_task_count")
    def task_count(self, obj):
        return obj._task_count
