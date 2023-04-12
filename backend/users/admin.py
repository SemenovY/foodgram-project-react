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



# from django.contrib import admin
# from django.contrib.auth.admin import UserAdmin
#
# from .models import User
#
#
# @admin.register(User)
# class CustomUserAdmin(UserAdmin):
#     list_display = (
#         'is_active', 'username', 'first_name', 'last_name', 'email',
#     )
#     fields = (
#         ('username', 'email', ),
#         ('first_name', 'last_name', ),
#         ('is_active', 'password', ),
#     )
#     fieldsets = []
#     search_fields = ('username', 'email',)
#     list_filter = ('is_active', 'first_name', 'email',)
#     save_on_top = True