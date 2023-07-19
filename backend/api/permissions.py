from rest_framework.permissions import BasePermission
from rest_framework.request import Request


class IsAuthorOrAdmin(BasePermission):
    """Проверка разрешений на уровне запроса."""

    def has_permission(self, request: Request, view) -> bool:
        return request.user.is_authenticated

    def has_object_permission(self, request: Request, view, obj) -> bool:
        return (request.user == obj.author
                or request.user.is_admin)
