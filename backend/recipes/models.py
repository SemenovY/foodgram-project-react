"""Модели для Ингредиентов, рецептов, тэгов"""
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models

User = get_user_model()


class Ingredient(models.Model):
    """Модель для ингредиентов"""

    name = models.CharField(max_length=200)
    measurement_unit = models.CharField(max_length=200)

    class meta:
        ordering = ['name']
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        constraints = [
            models.UniqueConstraint(
                fields=('name', 'measurement_unit'),
                name='ingredient_name_unit_unique',
            )
        ]

    def __str__(self):
        return f'{self.name}, {self.measurement_unit}.'


class Tag(models.Model):
    """Модель для тегов"""

    name = models.CharField(
        max_length=200,
        unique=True,
    )
    color = models.CharField(
        max_length=7,
        unique=True,
    )
    slug = models.SlugField(
        max_length=200,
        unique=True,
    )

    class Meta:
        ordering = ['name']
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name


class Recipe(models.Model):
    """Модель для рецептов"""

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipe',
    )
    name = models.CharField(
        max_length=200,
    )
    image = models.ImageField(
        upload_to='recipes/images/',
        blank=True,
        null=True,
    )
    text = models.TextField(
        verbose_name='Описание',
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='RecipeIngredient',
    )
    tags = models.ManyToManyField(
        Tag,
        related_name='recipes',
    )
    cooking_time = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(1, message='Мин. время приготовления 1 минута'),
        ]
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ('-pub_date',)

    def __str__(self):
        return self.name


class RecipeIngredient(models.Model):
    """Модель для связи ингредиента и рецепта"""

    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='recipe_ingredients',
        verbose_name='Рецепт',
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.PROTECT,
        related_name='recipe_ingredients',
        verbose_name='Ингредиент',
    )
    amount = models.PositiveIntegerField(
        verbose_name='Количество',
        validators=[
            MinValueValidator(
                1, message='Минимальное количество ингредиентов 1'
            )
        ],
    )

    class Meta:
        ordering = ['-id']
        verbose_name = 'Количество ингредиента'
        verbose_name_plural = 'Количество ингредиентов'
        constraints = [
            models.UniqueConstraint(
                fields=('recipe', 'ingredient'),
                name='unique_recipe_ingredient',
            )
        ]

    def __str__(self):
        return f'Рецепт: {self.recipe}. Ингредиент: {self.ingredient}, Количество: {self.amount}'
