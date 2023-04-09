"""Модели для ингредиентов, рецептов, тегов"""
from django.core.validators import MinValueValidator
from django.db import models
from users.models import User


class Ingredient(models.Model):
    """Модель для ингредиентов"""

    name = models.CharField(
        max_length=200,
        verbose_name='Название',
    )
    measurement_unit = models.CharField(
        max_length=200,
        verbose_name='Единицы измерения',
    )

    class Meta:
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
        verbose_name='Наименование',
    )
    color = models.CharField(
        max_length=7,
        unique=True,
        verbose_name='Цвет в HEX',
    )
    slug = models.SlugField(
        max_length=200,
        unique=True,
        verbose_name='Уникальный слаг',
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
        verbose_name='Автор',
    )
    name = models.CharField(
        max_length=200,
        verbose_name='Название',
    )
    image = models.ImageField(
        upload_to='recipes/images/',
        # blank=True,
        blank=False,
        null=True,
        verbose_name='Фотография рецепта',
    )
    text = models.TextField(
        verbose_name='Описание',
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='RecipeIngredient',
        verbose_name='Ингредиенты',
    )
    tags = models.ManyToManyField(
        Tag,
        related_name='recipes',
        verbose_name='Тэги',
    )
    cooking_time = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(
                1, message='Минимальное время приготовления 1 мин.'
            ),
        ],
        verbose_name='Время приготовления в минутах',
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации',
    )

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

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
            MinValueValidator(1, message='Минимальное кол-во ингредиентов 1')
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
        return f'Рецепт: {self.recipe}, Ингредиент: {self.ingredient}, Кол-во: {self.amount}'

# class Favorite(models.Model):
# """Модель списка избранного"""

#  class ShopingList(models.Model):
#     """Модель списка покупок"""
