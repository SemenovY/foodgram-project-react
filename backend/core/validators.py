"""Custom валидатор для проверки цвета HEX"""
from string import hexdigits

from django.core.exceptions import ValidationError


def hex_color_validator(color):
    """Проверка на длину и на разрешенные символы"""

    color = color.strip(' #')
    if len(color) != 6:
        raise ValidationError(
            f'Код цвета {color} не правильной длины ({len(color)}). '
            f'Длина должна быть 6 символов без учета # в начале '
            f'(например #FF0000).'
        )
    if not set(color).issubset(hexdigits):
        raise ValidationError(
            f'{color} содержит не шестнадцатиричные символы.'
            f'Используйте {hexdigits}.'
        )
    return '#' + color.upper()
