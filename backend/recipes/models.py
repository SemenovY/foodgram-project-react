import textwrap

from core.models import CoreModel
from core.validators import hex_color_validator
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

User = get_user_model()

CLS_NAME_LEN = settings.CLS_NAME_LEN
MAX_COOKING_TIME = settings.MAX_COOKING_TIME
MIN_COOKING_TIME = settings.MIN_COOKING_TIME
MAX_AMOUNT = settings.MAX_AMOUNT
MIN_AMOUNT = settings.MIN_AMOUNT


class Tag(models.Model):
    """Модель Тегов."""

    name = models.CharField(
        'Название',
        max_length=200,
        unique=True,
    )
    color = models.CharField(
        'Цвет в HEX',
        max_length=7,
    )
    slug = models.SlugField(
        'Уникальный слаг',
        max_length=200,
        unique=True,
    )

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self) -> str:
        return self.name[:CLS_NAME_LEN]

    def clean(self):
        self.color = hex_color_validator(self.color)
        return super().clean()


class Ingredient(models.Model):
    """Модель Ингредиентов."""

    name = models.CharField(
        'Название ингредиента',
        max_length=200,
    )
    measurement_unit = models.CharField(
        'Единица измерения',
        max_length=200,
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Ингридиент'
        verbose_name_plural = 'Ингридиенты'

    def __str__(self) -> str:
        return (
            f'Ингредиент: {self.name[:CLS_NAME_LEN]}, '
            f'измеряется в: {self.measurement_unit}'
        )


class Recipe(models.Model):
    """Модель Рецептов."""

    name = models.CharField(
        'Название рецепта',
        max_length=200,
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор',
    )
    image = models.ImageField('Картинка', upload_to='recipe_images/')
    text = models.TextField('Описание')
    ingredients = models.ManyToManyField(
        Ingredient,
        through='IngredientRecipe',
        related_name='recipes',
    )
    tags = models.ManyToManyField(
        Tag,
        through='TagRecipe',
        related_name='recipes',
    )
    cooking_time = models.PositiveSmallIntegerField(
        'Время приготовления',
        validators=(
            MinValueValidator(
                MIN_COOKING_TIME,
                'Время приготовления не может быть меньше минуты.',
            ),
            MaxValueValidator(
                MAX_COOKING_TIME,
                (
                    'Вы указали слишком длительное время приготовления '
                    '(максимум 10080 минут).'
                ),
            ),
        ),
    )
    pub_date = models.DateTimeField(
        'Дата публикации рецепта',
        auto_now_add=True,
        db_index=True,
    )

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        constraints = (
            models.UniqueConstraint(
                fields=('name', 'author'),
                name='unique_recipe_author',
            ),
        )

    def __str__(self) -> str:
        return (
            f'Название: {self.name[:CLS_NAME_LEN]} <-> '
            f'Описание: {textwrap.shorten(self.text, width=40)}. '
        )


class TagRecipe(models.Model):
    """Модель для связи Тега и Рецепта многие ко многим."""

    tag = models.ForeignKey(Tag, on_delete=models.CASCADE, verbose_name='Тег')
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, verbose_name='Рецепт'
    )

    class Meta:
        verbose_name = 'Тег рецепта'
        verbose_name_plural = 'Теги рецепта'
        constraints = (
            models.UniqueConstraint(
                fields=('recipe', 'tag'), name='unique_recipe_tag'
            ),
        )

    def __str__(self) -> str:
        return f'Рецепт: {self.recipe.name} содержит тег: {self.tag}'


class IngredientRecipe(models.Model):
    """Модель для связя Ингредиента и Рецепта многие ко многим."""

    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='amount',
        verbose_name='Ингредиент',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='ingredient',
        verbose_name='Рецепт',
    )
    amount = models.PositiveSmallIntegerField(
        'Количество',
        validators=(
            MinValueValidator(
                MIN_AMOUNT, 'Количество ингредиента не должно быть меньше 1.'
            ),
            MaxValueValidator(
                MAX_AMOUNT,
                (
                    'Вы указали слишком большое количество ингредиента '
                    '(максимальное значение 32767).'
                ),
            ),
        ),
    )

    class Meta:
        verbose_name = 'Ингридиент'
        verbose_name_plural = 'Количество ингридиентов'
        ordering = ('recipe',)
        constraints = (
            models.UniqueConstraint(
                fields=(
                    'recipe',
                    'ingredient',
                ),
                name='unique_ingredient_in_recipe',
            ),
        )

    def __str__(self) -> str:
        return (
            f'Рецепт <-> {self.recipe.name} '
            f'включает <-> {self.ingredient.name}'
        )


class Favorite(CoreModel):
    """Модель избранного."""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorite',
        verbose_name='Пользователь',
    )
    favorite_recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favorite_recipes',
        verbose_name='Избранный рецепт',
    )

    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранные'
        constraints = (
            models.UniqueConstraint(
                fields=('user', 'favorite_recipe'),
                name='unique_user_favorite_recipe',
            ),
        )

    def __str__(self) -> str:
        return (
            f'Пользователь: {self.user}, '
            f'избранные рецепты: {self.favorite_recipe}'
        )


class ShoppingCart(CoreModel):
    """Модель списка покупок."""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='shopping_cart',
        verbose_name='Пользователь',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='shopping_cart_recipe',
        verbose_name='Рецепт',
    )

    class Meta:
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Списки покупок'
        constraints = (
            models.UniqueConstraint(
                fields=('user', 'recipe'), name='unique_shopping_cart_recipe'
            ),
        )

    def __str__(self) -> str:
        return (
            f'Пользователь: {self.user.username}, '
            f'для покупок по рецепту: {self.recipe.name}'
        )
