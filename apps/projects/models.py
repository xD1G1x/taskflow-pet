from django.db import models
from django.conf import settings

# Create your models here.


class Project(models.Model):
    name = models.CharField(max_length=150)
    description = models.TextField(blank=True, default="")
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="owned_projects")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["owner", "name"],
                name="unique_project_name",
            ),
        ]

    def __str__(self) -> str:
        return self.name
