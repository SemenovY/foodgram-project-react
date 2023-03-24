"""User models."""
# abstract_user/users/models.py
# from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.db import models

# User = get_user_model()


class User(AbstractUser):
    """Custom user model."""

    email = models.EmailField(
        max_length=150,
        blank=False,
        unique=True,
        #        required=True,
    )

    #    username = (
    #        models.ForeignKey(
    #            User,
    #            on_delete=models.CASCADE,
    #            unique=True,
    #        ),
    #    )

    first_name = (
        models.TextField(
            max_length=150,
            #           required=True,
        ),
    )

    last_name = (
        models.TextField(
            max_length=150,
            #          required=True,
        ),
    )

    password = (
        models.TextField(
            max_length=150,
            #         required=True,
        ),
    )
