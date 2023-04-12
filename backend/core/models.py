"""Модель для приложения Core"""
from django.db.models import DateTimeField, Model


class CoreModel(Model):
    """Вспомогательная базовая модель для Recipes"""

    date_added = DateTimeField(
        'Дата добавления', auto_now_add=True, editable=False
    )

    class Meta:
        abstract = True
