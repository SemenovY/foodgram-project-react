"""Админ панель для рецептов и ингредиентов."""
from django.contrib import admin

from .models import Ingredient, Recipe, RecipeIngredient, Tag


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """Настройка админки для тэгов"""

    empty_value_display = '-empty-'
    list_display = ('pk', 'name', 'color', 'slug')
    list_filter = (
        'name',
        'slug',
    )
    search_fields = (
        'name',
        'slug',
    )


class IngredientsInRecipeInline(admin.TabularInline):
    model = Recipe.ingredients.through


class IngredientAdmin(admin.ModelAdmin):
    """Настройка списка ингредиентов для админки."""

    inlines = [
        IngredientsInRecipeInline,
    ]
    list_display = (
        'id',
        'name',
        'measurement_unit',
    )
    list_filter = ('name',)
    empty_value_display = '-empty-'


class RecipeAdmin(admin.ModelAdmin):
    inlines = [
        IngredientsInRecipeInline,
    ]
    exclude = ('ingredients',)
    # TODO:  list_display = ('id', 'author', 'name', 'count_favorite') Потом добавить
    list_display = (
        'id',
        'author',
        'name',
    )
    list_filter = ('author', 'name', 'tags')
    empty_value_display = '-empty-'


# TODO: readonly_fields = ('count_favorite',) потом добавить
# TODO: def count_favorite(self, obj): потом добавить
# TODO:     return obj.favorite.all().count() потом добавить
# TODO: count_favorite.short_description = 'Избранных' потом добавить


admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(RecipeIngredient)
# TODO: admin.site.register(Favorite) потом добавить
# TODO: admin.site.register(ShopingList)  потом добавить
