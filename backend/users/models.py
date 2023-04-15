"""Модель пользователя и подписки на авторов"""
from django.contrib.auth.models import AbstractUser
from django.db import models

from .validators import custom_user_validator, email_lowercase


class User(AbstractUser):
    """Кастомная модель пользователя"""

    username = models.CharField(
        verbose_name="Имя пользователя",
        max_length=150,
        unique=True,
        validators=(custom_user_validator,),
    )
    email = models.EmailField(
        verbose_name="Адрес электронной почты",
        max_length=254,
        unique=True,
    )
    first_name = models.CharField(
        verbose_name="Имя",
        max_length=150,
    )
    last_name = models.CharField(
        verbose_name="Фамилия",
        max_length=150,
    )
    password = models.CharField(
        verbose_name="Пароль",
        max_length=150,
    )
    is_active = models.BooleanField(
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
        constraints = (
            models.UniqueConstraint(
                fields=("username", "email"), name="unique_login_fields"
            ),
        )

    def __str__(self):
        return f"{self.username}: {self.email}"

    def clean(self):
        """Обработка полей"""
        self.email = email_lowercase(self.email)
        return super().clean()


class Subscriptions(models.Model):
    """Модель подписки на авторов"""

    user = models.ForeignKey(
        User,
        verbose_name="Подписчик",
        related_name="subscriber",
        on_delete=models.CASCADE,
    )
    author = models.ForeignKey(
        User,
        verbose_name="Автор рецепта",
        related_name="subscription",
        on_delete=models.CASCADE,
    )

    class Meta:
        ordering = ("-user",)
        verbose_name = "Подписка"
        verbose_name_plural = "Подписки"
        constraints = (
            models.UniqueConstraint(
                fields=("user", "author"), name="unique_subscription"
            ),
            models.CheckConstraint(
                check=~models.Q(author=models.F("user")),
                name="%(app_label)s_%(class)s_prevent_self_subscription",
            ),
        )

    def __str__(self):
        return f"{self.user.username} подписан на {self.author.username}"
