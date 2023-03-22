"""User models."""
# abstract_user/users/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Custom user model."""

    bio = models.TextField(
        'Биография',
        blank=True,
    )
    style = models.TextField(
        'Style',
        blank=True,
    )
