"""AbstractUser models."""
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Custom user model."""

    password = models.CharField('password', max_length=150)
