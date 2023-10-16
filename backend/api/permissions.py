from rest_framework.permissions import BasePermission
from rest_framework.request import Request


class IsAuthorOrAdmin(BasePermission):
    """Проверка разрешений на уровне запроса."""

    def has_permission(self, request: Request, view) -> bool:
        return request.user.is_authenticated

    def has_object_permission(self, request: Request, view, obj) -> bool:
        author = obj.traveler if hasattr(obj, 'traveler') else obj.author
        return (request.user == author
                or request.user.is_staff
                or request.user.is_superuser)
