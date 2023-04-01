"""Админ панель для рецептов и ингредиентов."""
from django.contrib import admin

from .models import Ingredient


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    """Настройка списка ингредиентов для админки."""

    list_display = (
        'id',
        'name',
        'measurement_unit',
    )
