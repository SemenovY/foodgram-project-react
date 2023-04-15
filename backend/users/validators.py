"""Валидатор для Custom User модели"""
import re

from django.core.exceptions import ValidationError


def email_lowercase(email):
    """Применяем lower для email модели User"""
    email = email or ""
    try:
        email_name, domain = email.strip().rsplit("@", 1)
    except ValueError:
        pass
    else:
        email = email_name.lower() + "@" + domain.lower()
    return email


def custom_user_validator(value):
    """Проверка поля username модели User"""

    if re.findall(r"[^\w.@+-]+", value):
        raise ValidationError("Только буквы, цифры и символы @/./+/-/")
