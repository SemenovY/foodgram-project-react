"""Панель администратора для модели User"""
from django.contrib import admin

from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """Настройка пользователя для админки."""

    list_display = (
        'username',
        'first_name',
        'last_name',
        'email',
        'is_subscribed',
    )

    list_filter = ('email', 'first_name', 'is_subscribed')
    search_fields = ('username', 'email')
