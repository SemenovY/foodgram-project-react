"""API сериализаторы для всех моделей"""
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.shortcuts import get_object_or_404
from djoser.serializers import UserCreateSerializer, UserSerializer
from drf_extra_fields.fields import Base64ImageField
from recipes.models import Ingredient, Recipe, RecipeIngredient, Tag
from rest_framework import serializers
from users.models import Follow, User

from .validators import color_validator


class CustomUserSerializer(UserSerializer):
    """Сериализатор для модели User"""

    is_subscribed = serializers.SerializerMethodField(
        method_name='get_is_subscribed'
    )

    class Meta:
        """Поля и модель сериализатора CustomUserSerializer"""

        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
        )

    def get_is_subscribed(self, obj):
        user = self.context['request'].user
        if user.is_anonymous:
            return False
        return Follow.objects.filter(user=user, author=obj).exists()


class CustomUserCreateSerializer(UserCreateSerializer):
    """Сериализатор для создания пользователя"""

    class Meta:
        """Поля и модель для сериализатора CustomUserCreateSerializer"""

        model = User
        fields = (
            'email',
            'username',
            'first_name',
            'last_name',
            'password',
        )
        extra_kwargs = {'password': {'write_only': True}}


class IngredientSerializer(serializers.ModelSerializer):
    """Сериализатор для модели ингредиентов"""

    class Meta:
        """Поля и модель для сериализатора IngredientSerializer"""

        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')


class TagSerializer(serializers.ModelSerializer):
    """Сериализатор для модели тэгов"""

    color = serializers.CharField(validators=[color_validator])

    class Meta:
        """Поля и модель для сериализатора TagSerializer"""

        model = Tag
        fields = (
            'id',
            'name',
            'color',
            'slug',
        )


class RecipeIngredientSerializer(serializers.ModelSerializer):
    """Сериализатор для модели RecipeIngredient"""

    id = serializers.SerializerMethodField(method_name='get_id')
    name = serializers.SerializerMethodField(method_name='get_name')
    measurement_unit = serializers.SerializerMethodField(
        method_name='get_measurement_unit'
    )

    def get_id(self, obj):
        return obj.ingredient.id

    def get_name(self, obj):
        return obj.ingredient.name

    def get_measurement_unit(self, obj):
        return obj.ingredient.measurement_unit

    class Meta:
        model = RecipeIngredient
        fields = ('id', 'name', 'measurement_unit', 'amount')


class CheckCreateRecipeSerializer(serializers.ModelSerializer):
    """Валидатор для минимально допустимого кол-ва ингредента"""

    id = serializers.IntegerField()
    amount = serializers.IntegerField(
        validators=(
            MinValueValidator(1, message='Нужен хотя бы один ингредиент'),
        )
    )

    class Meta:
        model = Ingredient
        fields = ('id', 'amount')


class RecipeSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Recipe"""

    ingredients = serializers.SerializerMethodField(
        method_name='get_ingredients'
    )
    tags = TagSerializer(many=True)
    image = Base64ImageField()
    author = UserSerializer(read_only=True)
    is_favorited = serializers.SerializerMethodField(
        method_name='get_is_favorited'
    )
    is_in_shopping_cart = serializers.SerializerMethodField(
        method_name='get_is_in_shopping_cart'
    )
    # TODO: перенести мету ниже

    class Meta:
        model = Recipe
        fields = '__all__'

    def validate_cooking_time(self, value):
        if not isinstance(value, int):
            raise serializers.ValidationError(
                'Время приготовления указывается целым числом'
            )
        if value < 1:
            raise serializers.ValidationError(
                'Время приготовления не может быть меньше 1 минуты'
            )
        return value

    def get_ingredients(self, obj):
        ingredients = RecipeIngredient.objects.filter(recipe=obj)

        serializer = RecipeIngredientSerializer(ingredients, many=True)

        return serializer.data

    # def get_is_favorited(self, obj):
    #     user = self.context['request'].user
    #     if user.is_anonymous:
    #         return False
    #     return Favorite.objects.filter(user=user, recipe=obj).exists()
    #
    # def get_is_in_shopping_cart(self, obj):
    #     user = self.context['request'].user
    #     if user.is_anonymous:
    #         return False
    #     return ShopingList.objects.filter(user=user, recipe=obj).exists()


class CreateRecipeSerializer(serializers.ModelSerializer):
    """Сериализатор для работы с рецептами"""

    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(), many=True
    )
    author = UserSerializer(read_only=True)
    ingredients = CheckCreateRecipeSerializer(many=True)
    image = Base64ImageField()
    cooking_time = serializers.IntegerField(
        validators=(
            MinValueValidator(
                1, message='Время приготовления не может быть меньше 1 минуты'
            ),
        )
    )

    class Meta:
        model = Recipe
        exclude = ('pub_date',)

    def validate_tags(self, value):
        if not value:
            raise exceptions.ValidationError('Укажите тег')
        return value

    def validate_ingredient(self, value):
        if not value:
            raise exceptions.ValidationError('Добавьте ингредиент')
        ingredients = [item['id'] for item in value]
        for ingredient in ingredients:
            if ingredients.count(ingredient) > 1:
                raise exceptions.ValidationError(
                    'Ингредиент уже присутствует в списке'
                )
        return value

    def create(self, validated_data):
        author = self.context.get('request').user
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')
        recipe = Recipe.objects.create(author=author, **validated_data)
        recipe.tags.set(tags)
        for ingredient in ingredients:
            amount = ingredient['amont']
            ingredient = get_object_or_404(Ingredient, pk=ingredient['id'])
            RecipeIngredient.objects.create(
                recipe=recipe, ingredient=ingredient, amount=amount
            )
        return recipe

    # def update(self, instance, validated_data):
    #     tags = validated_data.pop('tags', None)
    #     if tags is not None:
    #         instance.tags.set(tags)
    #     ingredients = validated_data.pop('ingredients', None)
    #     if ingredients is not None:
    #         instance.ingredients.clear()
    #         for ingredient in ingredients:
    #             amount = ingredient['amount']
    #             ingredient = get_object_or_404(Ingredient, pk=ingredient['id'])
    #             RecipeIngredient.objects.update_or_create(
    #                 recipe=instance,
    #                 ingredient=ingredient,
    #                 defaults={'amount': amount},
    #             )
    #     return super().update(instance, validated_data)

    def to_representation(self, instance):
        serializer = RecipeSerializer(
            instance, context={'request': self.context.get('request')}
        )
        return serializer.data


#
#
#
#
#
#
#
#
# TODO: Переписать сериализатор
# class UserFollowSerializer(UserSerializer):
#     """Сериализатор вывода авторов на которых только что подписался пользователь.
#     В выдачу добавляются рецепты."""
#
#     recipes = serializers.SerializerMethodField(method_name='get_recipes')
#     recipes_count = serializers.SerializerMethodField(
#         method_name='get_recipes_count'
#     )
#
#     class Meta:
#         model = MyUser
#         fields = (
#             'email',
#             'id',
#             'username',
#             'first_name',
#             'last_name',
#             'is_subscribed',
#             'recipes',
#             'recipes_count',
#         )
#         read_only_fields = ('__all__',)
#
#     def get_srs(self):
#         return ShortRecipeSerializer
#
#     def get_recipes(self, obj):
#         author_recipes = Recipe.objects.filter(author=obj)
#         if 'recipes_limit' in self.context.get('request').GET:
#             recipes_limit = self.context.get('request').GET['recipes_limit']
#             author_recipes = author_recipes[: int(recipes_limit)]
#         if author_recipes:
#             serializer = self.get_srs()(
#                 author_recipes,
#                 context={'request': self.context.get('request')},
#                 many=True,
#             )
#             return serializer.data
#         return []
#
#     def get_recipes_count(self, obj):
#         return Recipe.objects.filter(author=obj).count()
#
#
#
#
# class ShortRecipeSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Recipe
#         fields = ('id', 'name', 'image', 'cooking_time')
