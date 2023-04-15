"""Панель администратора для модели User"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Subscriptions, User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    """Панель администратора для модели User"""

    list_display = (
        "is_active",
        "username",
        "first_name",
        "last_name",
        "email",
    )
    fields = (
        (
            "username",
            "email",
        ),
        (
            "first_name",
            "last_name",
        ),
        (
            "is_active",
            "password",
        ),
    )
    fieldsets = []
    list_filter = (
        "is_active",
        "first_name",
        "email",
    )
    search_fields = (
        "username",
        "email",
    )
    save_on_top = True


@admin.register(Subscriptions)
class SubscriptionsAdmin(admin.ModelAdmin):
    """Панель администратора для модели Subscriptions"""

    list_display = (
        "user",
        "author",
    )
    search_fields = (
        "user",
        "author",
    )
    save_on_top = True
