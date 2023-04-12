"""Модель пользователя и подписки на авторов"""
from django.contrib.auth.models import AbstractUser
from django.db import models

from .validators import username_validator


class User(AbstractUser):
    """Кастомная модель пользователя"""

    username = models.CharField(
        max_length=150,
        unique=True,
        verbose_name='Уникальное имя пользователя',
        validators=(username_validator,),
    )
    email = models.EmailField(
        unique=True,
        max_length=254,
        verbose_name='Адрес электронной почты',
    )
    first_name = models.CharField(
        max_length=150,
        verbose_name='Имя',
    )
    last_name = models.CharField(
        max_length=150,
        verbose_name='Фамилия',
    )
    password = models.CharField(
        max_length=150,
        verbose_name='Пароль',
    )
    is_subscribed = models.BooleanField(
        verbose_name='Подписан',
        default=True,
    )
    # TODO тестирую без этих полей
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [
        'username',
        'first_name',
        'last_name',
    ]

    class Meta:
        ordering = ('username',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        constraints = (
            models.UniqueConstraint(
                fields=('username', 'email'), name='unique_login_fields'
            ),
        )

    def __str__(self):
        return f'{self.username}: {self.email}'


class Subscriptions(models.Model):
    """Модель подписки на авторов"""

    user = models.ForeignKey(
        User,
        related_name='subscriber',
        on_delete=models.CASCADE,
        verbose_name='Подписчик',
    )
    author = models.ForeignKey(
        User,
        related_name='subscription',
        on_delete=models.CASCADE,
        verbose_name='Автор рецепта',
    )

    class Meta:
        ordering = ('-user',)
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        constraints = (
            models.UniqueConstraint(
                fields=('user', 'author'), name='unique_subscription'
            ),
            models.CheckConstraint(
                check=~models.Q(author=models.F('user')),
                name='%(app_label)s_%(class)s_prevent_self_subscription',
            ),
        )

    def __str__(self):
        return f'{self.user} подписан на {self.author}'
