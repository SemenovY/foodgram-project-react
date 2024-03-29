"""Основные сериализаторы проекта"""
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import transaction
from djoser.serializers import (PasswordSerializer, UserCreateSerializer,
                                UserSerializer)
from drf_extra_fields.fields import Base64ImageField
from recipes.models import (Favorite, Ingredient, IngredientRecipe, Recipe,
                            ShoppingCart, Tag)
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from users.models import Subscriptions

from backend.settings import (MAX_AMOUNT, MAX_COOKING_TIME, MIN_AMOUNT,
                              MIN_COOKING_TIME)

User = get_user_model()


class CustomUserSerializer(UserSerializer):
    """Сериализатор для CustomUser, выдача, добавлено поле is_subscribed"""

    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            "email",
            "id",
            "username",
            "first_name",
            "last_name",
            "is_subscribed",
        )

    def get_is_subscribed(self, obj):
        """
        Проверка подписки пользователей, проверяем подписан ли
        текущий пользователь на просматриваемого пользователя.
        """

        user = self.context["request"].user
        return (
            user.is_authenticated
            and user.subscriber.filter(author=obj).exists()
        )


class CustomUserCreateSerializer(UserCreateSerializer):
    """Сериализатор для создания пользователей"""

    class Meta:
        model = User
        fields = (
            "email",
            "id",
            "username",
            "first_name",
            "last_name",
            "password",
        )


class CustomPasswordSerializer(PasswordSerializer):
    """Сериализатор для смены пароля"""

    current_password = serializers.CharField(required=True)


class ShortRecipeSerializer(serializers.ModelSerializer):
    """
    Сериализатор модели Recipe,
    укороченный набор полей для эндпоинтов: списка покупок и подписок.
    """

    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = (
            "id",
            "name",
            "image",
            "cooking_time",
        )
        read_only_fields = ("id", "name", "image", "cooking_time")


class UserSubscribeSerializer(CustomUserSerializer):
    """Сериализатор вывода авторов на которых подписан текущий пользователь"""

    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            "email",
            "id",
            "username",
            "first_name",
            "last_name",
            "is_subscribed",
            "recipes",
            "recipes_count",
        )
        read_only_fields = (
            "email",
            "username",
            "first_name",
            "last_name",
        )

    def get_is_subscribed(*args):
        """Проверка подписки пользователей, по умолчанию всегда будет True"""
        return True

    def get_recipes(self, obj):
        """Определение поля recipes, передача параметра recipes_limit"""
        request = self.context.get("request")
        if request is not None:
            limit = request.GET.get("recipes_limit")
        else:
            limit = self.context.get("recipes_limit")
        recipes = obj.recipes.all()
        if limit:
            recipes = recipes[: int(limit)]
        return ShortRecipeSerializer(recipes, many=True).data

    def get_recipes_count(self, obj):
        """Показывает общее кол-во рецептов у каждого автора"""
        return obj.recipes.count()


class SubscribeSerializer(serializers.ModelSerializer):
    """Управления подписками"""

    class Meta:
        model = Subscriptions
        fields = ("user", "author")
        validators = (
            UniqueTogetherValidator(
                queryset=Subscriptions.objects.all(),
                fields=(
                    "user",
                    "author",
                ),
                message="Вы уже подписаны на этого автора!",
            ),
        )

    def validate(self, data):
        if data.get("user") == data.get("author"):
            raise serializers.ValidationError(
                "Нельзя подписаться на самого себя!"
            )
        return data


class TagSerializer(serializers.ModelSerializer):
    """Сериалайзер для получения тега или списка тегов"""

    class Meta:
        model = Tag
        fields = ("id", "name", "color", "slug")


class IngredientSerializer(serializers.ModelSerializer):
    """Сериалайзер для получения ингредиента или списка ингредиентов"""

    class Meta:
        model = Ingredient
        fields = ("id", "name", "measurement_unit")


class IngredientInRecipeSerializer(serializers.ModelSerializer):
    """Сериализатор для отображения ингредиентов в рецепте"""

    id = serializers.IntegerField(
        source="ingredient.id",
    )
    name = serializers.ReadOnlyField(
        source="ingredient.name",
    )
    measurement_unit = serializers.ReadOnlyField(
        source="ingredient.measurement_unit",
    )

    class Meta:
        model = IngredientRecipe
        fields = ("id", "name", "measurement_unit", "amount")


class AddIngredientToRecipeSerializer(serializers.ModelSerializer):
    """Сериалайзер для добавления ингредиентов в рецепт"""

    id = serializers.PrimaryKeyRelatedField(queryset=Ingredient.objects.all())
    amount = serializers.IntegerField(
        write_only=True,
        validators=(
            MinValueValidator(
                MIN_AMOUNT, "Количество ингредиента не должно быть меньше 1."
            ),
            MaxValueValidator(
                MAX_AMOUNT,
                ("Вы указали слишком большое количество ингредиента"),
            ),
        ),
    )

    class Meta:
        model = IngredientRecipe
        fields = ("id", "amount")


class GetRecipeSerializer(serializers.ModelSerializer):
    """Сериалайзер для получения рецепта или списка рецептов"""

    tags = TagSerializer(read_only=True, many=True)
    image = Base64ImageField()
    author = CustomUserSerializer(read_only=True)
    ingredients = serializers.SerializerMethodField()
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = (
            "id",
            "tags",
            "author",
            "ingredients",
            "is_favorited",
            "is_in_shopping_cart",
            "name",
            "image",
            "text",
            "cooking_time",
        )

    def get_ingredients(self, obj):
        ingredients = IngredientRecipe.objects.filter(recipe=obj)
        return IngredientInRecipeSerializer(ingredients, many=True).data

    def get_is_favorited(self, obj):
        request = self.context.get("request")
        if request.user:
            return (
                (request is not None) and request.user.is_authenticated
            ) and Favorite.objects.filter(
                favorite_recipe=obj, user=request.user
            ).exists()

    def get_is_in_shopping_cart(self, obj):
        request = self.context.get("request")
        if request is None or request.user.is_anonymous:
            return False
        user = request.user
        return ShoppingCart.objects.filter(recipe=obj, user=user).exists()


class CreateRecipeSerializer(GetRecipeSerializer):
    """Сериализатор для создания, удаления и обновления рецепта"""

    cooking_time = serializers.IntegerField(
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
    ingredients = AddIngredientToRecipeSerializer(many=True)
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(), many=True
    )
    image = Base64ImageField(max_length=None, use_url=True)

    class Meta:
        model = Recipe
        fields = (
            "id",
            "tags",
            "author",
            "ingredients",
            "name",
            "image",
            "text",
            "cooking_time",
        )

    def validate(self, data):
        """Проверка данных при создании/редактировании рецепта"""
        request = self.context.get("request")
        user = request.user
        name = data.get("name")
        if (
            request.method == "POST"
            and Recipe.objects.filter(author=user, name=name).exists()
        ):
            raise ValidationError("Рецепт с таким именем уже существует!")

        ingredients = data["ingredients"]
        if not ingredients:
            raise ValidationError("Необходим хотя бы один ингредиент!")
        ing_list = []
        for ingredient in ingredients:
            ing_id = ingredient["id"]
            if ing_id in ing_list:
                raise ValidationError("Выберите различные ингредиенты!")
            ing_list.append(ing_id)
        return data

    def create_ingredients(self, ingredients, recipe):
        """Функция добавления списка игредиентов в рецепт"""
        IngredientRecipe.objects.bulk_create(
            [
                IngredientRecipe(
                    ingredient=ingredient["id"],
                    recipe=recipe,
                    amount=ingredient["amount"],
                )
                for ingredient in ingredients
            ]
        )

    @transaction.atomic
    def create(self, validated_data):
        """Создание рецепта"""
        ingredients = validated_data.pop("ingredients")
        tags = validated_data.pop("tags")
        user = self.context.get("request").user
        recipe = Recipe.objects.create(author=user, **validated_data)
        recipe.tags.set(tags)
        self.create_ingredients(ingredients, recipe)
        recipe.save()
        return recipe

    @transaction.atomic
    def update(self, instance, validated_data):
        """Обновление рецепта"""
        instance.name = validated_data.pop("name", instance.name)
        instance.cooking_time = validated_data.pop(
            "cooking_time",
            instance.cooking_time,
        )
        instance.image = validated_data.pop("image", instance.image)
        ingredients = validated_data.pop("ingredients")
        IngredientRecipe.objects.filter(recipe=instance).delete()
        self.create_ingredients(ingredients, instance)
        tags = validated_data.pop("tags")
        instance.tags.set(tags)
        instance.text = validated_data.pop("text", instance.text)
        return super().update(instance, validated_data)

    def to_representation(self, instance):
        """ "Отображение рецепта"""
        serializer = GetRecipeSerializer(
            instance, context={"request": self.context.get("request")}
        )
        return serializer.data


class FavoriteSerializer(serializers.ModelSerializer):
    """Сериализатор для добавления и удаления избранных рецептов"""

    id = serializers.IntegerField(source="favorite_recipe.id", read_only=True)
    name = serializers.CharField(source="favorite_recipe.name", read_only=True)
    image = Base64ImageField(
        source="favorite_recipe.image",
        read_only=True,
        max_length=None,
        use_url=True,
    )
    cooking_time = serializers.IntegerField(
        source="favorite_recipe.cooking_time", read_only=True
    )

    class Meta:
        model = Favorite
        fields = ("id", "name", "image", "cooking_time")

    def validate(self, data):
        """Проверка валидации"""
        user = User.objects.get(id=self.context["request"].user.id)
        favorite_recipe = Recipe.objects.get(id=self.context["recipe_id"])
        if Favorite.objects.filter(
            user=user, favorite_recipe=favorite_recipe
        ).exists():
            raise serializers.ValidationError("Данный рецепт уже в избранном!")
        return data


class ShoppingCartSerializer(serializers.ModelSerializer):
    """Сериализатор для добавления и удаления рецептов в список покупок"""

    id = serializers.IntegerField(source="recipe.id", read_only=True)
    name = serializers.CharField(source="recipe.name", read_only=True)
    image = Base64ImageField(
        source="recipe.image", read_only=True, max_length=None, use_url=True
    )
    cooking_time = serializers.IntegerField(
        source="recipe.cooking_time", read_only=True
    )

    class Meta:
        model = ShoppingCart
        fields = ("id", "name", "image", "cooking_time")

    def validate(self, data):
        """Валидация"""
        user = User.objects.get(id=self.context["request"].user.id)
        recipe = Recipe.objects.get(id=self.context["recipe_id"])
        if ShoppingCart.objects.filter(user=user, recipe=recipe).exists():
            raise serializers.ValidationError(
                "Рецепт уже добавлен в список покупок."
            )
        return data
