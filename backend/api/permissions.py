from rest_framework.permissions import BasePermission


class IsAuthorOrAdmin(BasePermission):
    """Проверка разрешений на уровне запроса."""
    def has_permission(self, request, view, obj):
        return (request.user == obj.author
                and request.user.is_admin)
