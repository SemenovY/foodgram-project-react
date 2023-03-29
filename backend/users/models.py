"""User model"""
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Custom user model."""

    email = models.EmailField(
        unique=True,
        db_index=True,
        max_length=settings.LENGTH_OF_FIELDS_EMAIL,
        verbose_name='Электронная почта',
        help_text='Адрес электронной почты',
    )

    first_name = models.CharField(
        max_length=settings.LENGTH_OF_FIELDS_USER,
        verbose_name='Имя пользователя',
        help_text='Имя пользователя',
    )

    last_name = models.CharField(
        max_length=settings.LENGTH_OF_FIELDS_USER,
        verbose_name='Фамилия',
        help_text='Фамилия',
    )

    password = models.CharField(
        max_length=settings.LENGTH_OF_FIELDS_USER,
        verbose_name='Пароль',
        help_text='Пароль пользователя',
    )

    class Meta:
        ordering = ('username',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username
