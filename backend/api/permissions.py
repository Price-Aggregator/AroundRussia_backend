from rest_framework.permissions import BasePermission


class IsAuthorOrAdmin(BasePermission):
    """Проверка разрешений на уровне запроса."""
    def has_object_permission(self, request, view, obj):
        return (request.user == obj.author
                or request.user.is_admin)
