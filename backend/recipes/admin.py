"""Админ панель для рецептов тегов и ингредиентов"""
from django.conf import settings
from django.contrib.admin import ModelAdmin, TabularInline, register, site

from .models import Ingredient, IngredientRecipe, Recipe, Tag, TagRecipe

site.site_header = 'Администрирование портала Foodgram'

EMPTY_VALUE_DISPLAY = settings.EMPTY_VALUE_DISPLAY
NUM_SHOW = settings.NUM_SHOW


class TagInline(TabularInline):
    """Класс для отображения тэгов в модели рецептов"""

    model = TagRecipe
    extra = NUM_SHOW


class IngredientInline(TabularInline):
    """Класс для отображения ингредиентов в модели рецептов"""

    model = IngredientRecipe
    extra = NUM_SHOW


@register(IngredientRecipe)
class LinksIngRecAdmin(ModelAdmin):
    pass


@register(TagRecipe)
class LinksTagRecAdmin(ModelAdmin):
    pass


@register(Tag)
class TagAdmin(ModelAdmin):
    list_display = ('name', 'slug', 'color')
    list_filter = ('name',)


@register(Ingredient)
class IngredientAdmin(ModelAdmin):
    list_display = ('name', 'measurement_unit')
    list_filter = ('name',)
    save_on_top = True
    empty_value_display = EMPTY_VALUE_DISPLAY


@register(Recipe)
class RecipeAdmin(ModelAdmin):
    def favorite_recipes_count(self, obj):
        return obj.favorite_recipes.count()

    favorite_recipes_count.short_description = 'Сколько в избранном'
    list_display = ('name', 'author', 'favorite_recipes_count')
    list_filter = (
        'name',
        'author__username',
        'tags__name',
    )
    search_fields = (
        'name',
        'author__username',
        'tags__name',
    )
    inlines = (
        IngredientInline,
        TagInline,
    )
    save_on_top = True
    empty_value_display = EMPTY_VALUE_DISPLAY
