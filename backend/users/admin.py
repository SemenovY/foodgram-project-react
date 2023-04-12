"""Панель администратора для модели User"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    """Настройка пользователя для админки"""

    list_display = (
        'is_active', 'username', 'first_name', 'last_name', 'email',
    )
    fields = (
        ('username', 'email', ),
        ('first_name', 'last_name', ),
        ('is_active', 'password', ),
    )
    fieldsets = []
    list_filter = ('is_active', 'first_name', 'email',)
    search_fields = ('username', 'email',)
    save_on_top = True
