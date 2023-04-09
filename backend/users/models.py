"""Модель пользователя и подписчика"""
from django.contrib.auth.models import AbstractUser
from django.core import validators
from django.db import models


class User(AbstractUser):
    """Кастомная модель пользователя"""

    username = models.CharField(
        max_length=150,
        unique=True,
        verbose_name="Логин",
        validators=[validators.RegexValidator(regex="/^[a-z ,.'-]+$/i")],
    )
    email = models.EmailField(
        unique=True,
        max_length=254,
        verbose_name="Почта",
    )
    first_name = models.CharField(
        max_length=150,
        verbose_name="Имя",
    )
    last_name = models.CharField(
        max_length=150,
        verbose_name="Фамилия",
    )
    password = models.CharField(
        max_length=150,
        verbose_name="Пароль",
    )
    is_subscribed = models.BooleanField(
        verbose_name="Подписан",
        default=True,
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = [
        "username",
        "first_name",
        "last_name",
    ]

    class Meta:
        ordering = ("username",)
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.username

# class Follow(models.Model):
#    """Модель подписки на пользователей"""

#    pass
