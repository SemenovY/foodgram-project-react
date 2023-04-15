"""Модели тегов, рецептов, ингредиентов и взаимозависимостей"""
import textwrap

from core.models import CoreModel
from core.validators import hex_color_validator
from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models.functions import Length

from backend.settings import (MAX_AMOUNT, MAX_COOKING_TIME, MIN_AMOUNT,
                              MIN_COOKING_TIME, NAME_LEN)

User = get_user_model()

models.CharField.register_lookup(Length)


class Tag(models.Model):
    """Модель Тегов"""

    name = models.CharField(
        verbose_name="Тег",
        max_length=200,
        unique=True,
    )
    color = models.CharField(
        verbose_name="Цвет в HEX",
        max_length=7,
        unique=True,
    )
    slug = models.SlugField(
        verbose_name="Уникальный слаг",
        max_length=200,
        unique=True,
    )

    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = "Теги"

    def __str__(self):
        return self.name[:NAME_LEN]

    def clean(self):
        """Обработка полей"""
        self.color = hex_color_validator(self.color)
        return super().clean()


class Ingredient(models.Model):
    """Модель для ингредиентов"""

    name = models.CharField(
        verbose_name="Название ингредиента",
        max_length=200,
    )
    measurement_unit = models.CharField(
        verbose_name="Единица измерения",
        max_length=200,
    )

    class Meta:
        """Проверка полей"""

        ordering = ("name",)
        verbose_name = "Ингредиент"
        verbose_name_plural = "Ингредиенты"
        constraints = (
            models.UniqueConstraint(
                fields=("name", "measurement_unit"),
                name="unique_for_ingredient",
            ),
            models.CheckConstraint(
                check=models.Q(name__length__gt=0),
                name="\n%(app_label)s_%(class)s_name is empty\n",
            ),
            models.CheckConstraint(
                check=models.Q(measurement_unit__length__gt=0),
                name="\n%(app_label)s_%(class)s_measurement_unit is empty\n",
            ),
        )

    def __str__(self):
        return f"{self.name[:NAME_LEN]}, измеряется в: {self.measurement_unit}"


class Recipe(models.Model):
    """Модель Рецептов"""

    name = models.CharField(
        verbose_name="Название рецепта",
        max_length=200,
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="recipes",
        verbose_name="Автор",
    )
    image = models.ImageField(
        verbose_name="Изображение рецепта",
        upload_to="recipe_images/",
    )
    text = models.TextField(
        verbose_name="Описание",
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through="IngredientRecipe",
        related_name="recipes",
    )
    tags = models.ManyToManyField(
        Tag,
        through="TagRecipe",
        related_name="recipes",
    )
    cooking_time = models.PositiveSmallIntegerField(
        verbose_name="Время приготовления",
        validators=(
            MinValueValidator(
                MIN_COOKING_TIME,
                "Время приготовления не может быть меньше минуты",
            ),
            MaxValueValidator(
                MAX_COOKING_TIME,
                ("Вы указали слишком длительное время приготовления "),
            ),
        ),
    )
    pub_date = models.DateTimeField(
        "Дата публикации рецепта",
        auto_now_add=True,
        db_index=True,
    )

    class Meta:
        """Проверка полей"""

        ordering = ("-pub_date",)
        verbose_name = "Рецепт"
        verbose_name_plural = "Рецепты"
        constraints = (
            models.UniqueConstraint(
                fields=("name", "author"),
                name="unique_recipe_author",
            ),
        )

    def __str__(self):
        return (
            f"{self.name[:NAME_LEN]} <==> "
            f"Описание: {textwrap.shorten(self.text, width=40)}. "
        )


class TagRecipe(models.Model):
    """Модель для связи Тега и Рецепта"""

    tag = models.ForeignKey(Tag, on_delete=models.CASCADE, verbose_name="Тег")
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name="Рецепт",
    )

    class Meta:
        """Проверка полей"""

        verbose_name = "Тег рецепта"
        verbose_name_plural = "Теги рецепта"
        constraints = (
            models.UniqueConstraint(
                fields=("recipe", "tag"), name="unique_recipe_tag"
            ),
        )

    def __str__(self):
        return f"Рецепт: {self.recipe.name} содержит тег: {self.tag}"


class IngredientRecipe(models.Model):
    """Модель для связи Ингредиента и Рецепта"""

    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name="amount",
        verbose_name="Ингредиент",
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name="ingredient",
        verbose_name="Рецепт",
    )
    amount = models.PositiveSmallIntegerField(
        "Количество",
        validators=(
            MinValueValidator(
                MIN_AMOUNT, "Количество ингредиента не должно быть меньше 1."
            ),
            MaxValueValidator(
                MAX_AMOUNT,
                ("Указано слишком большое количество ингредиента"),
            ),
        ),
    )

    class Meta:
        """Проверка полей"""

        ordering = ("recipe",)
        verbose_name = "Ингредиент"
        verbose_name_plural = "Количество ингредиентов"
        constraints = (
            models.UniqueConstraint(
                fields=(
                    "recipe",
                    "ingredient",
                ),
                name="unique_ingredient_in_recipe",
            ),
        )

    def __str__(self):
        return (
            f"Рецепт <==> {self.recipe.name} "
            f"содержит <==> {self.ingredient.name}"
        )


class Favorite(CoreModel):
    """Модель для добавления рецепта в избранное"""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="favorite",
        verbose_name="Пользователь",
    )
    favorite_recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name="favorite_recipes",
        verbose_name="Избранный рецепт",
    )

    class Meta:
        """Проверка полей"""

        verbose_name = "Избранное"
        verbose_name_plural = "Избранные"
        constraints = (
            models.UniqueConstraint(
                fields=("user", "favorite_recipe"),
                name="unique_user_favorite_recipe",
            ),
        )

    def __str__(self):
        return (
            f"Пользователь: {self.user}, "
            f"избранные рецепты: {self.favorite_recipe}"
        )


class ShoppingCart(CoreModel):
    """Модель для списка покупок"""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="shopping_cart",
        verbose_name="Пользователь",
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name="shopping_cart_recipe",
        verbose_name="Рецепт",
    )

    class Meta:
        """Проверка полей"""

        verbose_name = "Список покупок"
        verbose_name_plural = "Списки покупок"
        constraints = (
            models.UniqueConstraint(
                fields=("user", "recipe"), name="unique_shopping_cart_recipe"
            ),
        )

    def __str__(self):
        return (
            f"Пользователь: {self.user.username}, "
            f"для покупок: {self.recipe.name}"
        )
