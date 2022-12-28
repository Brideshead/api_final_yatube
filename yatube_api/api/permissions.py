from django.http import HttpRequest
from rest_framework import permissions


class AuthorPermission(permissions.BasePermission):
    """
    Настрока прав разрешений.

    Если запрос безопасный, и пользователь является автором,
    то доступ разрешаем и возвращаем значение True.
    """

    def has_object_permission(
        self,
        request: HttpRequest,
        _view: None,
        obj: object,
    ) -> bool:
        del _view

        return (
            request.method in permissions.SAFE_METHODS
            or obj.author == request.user,
        )
