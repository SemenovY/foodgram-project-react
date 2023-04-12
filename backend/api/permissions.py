"""Разрешения для гостя, админа, авторизованного пользователя"""
from rest_framework.permissions import SAFE_METHODS, BasePermission


class BaseActivePermission(BasePermission):
    """Базовый класс разрешений"""

    message = 'Вам необходимо зарегестрироваться'

    def has_permission(self, request, view):
        return (
            request.method in SAFE_METHODS
            or request.user.is_authenticated
            and request.user.is_active
        )


class IsAdminOrReadOnly(BaseActivePermission):
    """Права администратора или только на чтение."""

    message = 'Доступ только для администратора сайта'

    def has_object_permission(self, request, view, obj):
        return request.method in SAFE_METHODS or (
            request.user.is_authenticated and request.user.is_staff
        )


class AuthorAdminOrReadOnly(BaseActivePermission):
    """Права автора, администратора или только на чтение."""

    message = 'Недостаточно прав, аутентифицируйтесь!'

    def has_object_permission(self, request, view, obj):
        return request.method in SAFE_METHODS or (
            request.user.is_authenticated
            and request.user.is_active
            and (request.user == obj.author or request.user.is_staff)
        )
