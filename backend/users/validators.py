"""Валидатор для Custom User"""
import re

from django.core.exceptions import ValidationError


def custom_user_validator(value):
    """Проверка поля username модели User на допустимые символы"""

    if re.findall(r'[^\w.@+-]+', value):
        raise ValidationError(
            'Только буквы, цифры и символы @/./+/-/'
        )
