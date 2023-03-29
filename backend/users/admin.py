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
        'is_active',
    )
    list_filter = ('is_active',)
    search_fields = ('email__istartswith', 'username__istartswith')
    fieldsets = (
        (
            None,
            {
                'fields': (
                    'username',
                    'first_name',
                    'last_name',
                    'email',
                    'is_active',
                )
            },
        ),
    )
