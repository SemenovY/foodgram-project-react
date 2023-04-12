"""Валидатор для Custom User"""
import re

from django.core.exceptions import ValidationError


def username_validator(value):
    """Проверка поля username модели user на допустимые символы"""

    if re.findall(r'[^\w.@+-]+', value):
        raise ValidationError(
            'Используйте буквы, цифры и символы @/./+/-/ при создании имени'
        )
