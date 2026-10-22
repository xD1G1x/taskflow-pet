from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsProjectOwnerOrAssigneeReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj): # type: ignore[override]
        if request.method in SAFE_METHODS:
            return True

        is_owner = obj.project.owner == request.user
        is_assignee = obj.assignees.filter(id=request.user.id).exists()

        if is_owner:
            return True

        if is_assignee and request.method == "PATCH":
            return True   

        return False
    
class IsAuthorOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.author == request.user