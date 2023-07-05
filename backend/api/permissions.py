from rest_framework.permissions import BasePermission


class AuthorPermission(BasePermission):
    """Разрешение на доступ только для автора."""

    def has_permission(self, request, view, obj):
        return obj.author == request.user
