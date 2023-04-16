"""Панель администратора для модели User"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.core.exceptions import ValidationError
from django.forms import ModelForm
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


class SuscriptionsForm(ModelForm):
    """Проверка подписки на самого себя"""

    class Meta:
        """Метаданные для формы подписки"""

        model = Subscriptions
        fields = (
            "user",
            "author",
        )

    def clean(self):
        """Функция проверки подписки на самого себя"""
        cleaned_data = super(SuscriptionsForm, self).clean()
        if cleaned_data.get("user") == cleaned_data.get("author"):
            raise ValidationError("Нельзя подписаться на самого себя!")
        return cleaned_data


@admin.register(Subscriptions)
class SubscriptionsAdmin(admin.ModelAdmin):
    """Панель администратора для модели Subscriptions"""

    form = SuscriptionsForm
    list_display = (
        "user",
        "author",
    )
    search_fields = (
        "user",
        "author",
    )
