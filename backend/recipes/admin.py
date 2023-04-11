"""Админ панель для рецептов тегов и ингредиентов"""
from django.contrib import admin

from .models import Ingredient, Recipe, RecipeIngredient, Tag, Favorite, ShopingList


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """Настройка админки для тегов"""

    list_display = ('pk', 'name', 'color', 'slug')
    list_filter = (
        'name',
        'slug',
    )
    search_fields = (
        'name',
        'slug',
    )
    empty_value_display = '-empty-'


class IngredientsInRecipeInline(admin.TabularInline):
    """Микс инлайн для рецепта и ингредиента"""

    model = Recipe.ingredients.through


class IngredientAdmin(admin.ModelAdmin):
    """Настройка списка ингредиентов для админки"""

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
    """Настройка админпанели для рецептов"""

    inlines = [
        IngredientsInRecipeInline,
    ]
    exclude = ('ingredients',)
    list_display = ('id', 'author', 'name', 'count_favorite')

    list_filter = ('author', 'name', 'tags')
    empty_value_display = '-empty-'

    readonly_fields = ('count_favorite',)

    def count_favorite(self, obj):
        return obj.favorite.all().count()

    count_favorite.short_description = 'Избранных'


admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(RecipeIngredient)
admin.site.register(Favorite)
admin.site.register(ShopingList)
