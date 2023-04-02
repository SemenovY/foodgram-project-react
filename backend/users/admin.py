"""Admin panel for abstractuser models."""
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
        'password',  # Удалить при рефакторинге
        'is_active',
    )

    list_filter = ('email', 'first_name', 'is_subscribed')
    search_fields = ('username', 'email')
