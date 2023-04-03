"""API сериализаторы для всех моделей"""
from djoser.serializers import UserCreateSerializer, UserSerializer
from recipes.models import Ingredient, Recipe, Tag
from rest_framework import serializers
from users.models import User


class CustomUserSerializer(UserSerializer):
    """Сериализатор для модели User"""

    class Meta:
        """Поля и модель сериализатора"""

        model = User
        fields = (
            'email',
            'id',  # TODO это поле возможно надо удалить
            'username',
            'first_name',
            'last_name',
            #            'is_subscribed', TODO: Дописать функцию
        )


class CustomUserCreateSerializer(UserCreateSerializer):
    """Сериализатор для создания пользователя"""

    class Meta:
        """Поля и модель для сериализатора CreateUser"""

        model = User
        fields = (
            'email',
            'id',  # TODO удалить это поле или проверить нужно ли
            'username',
            'first_name',
            'last_name',
            'password',
        )


class IngredientSerializer(serializers.ModelSerializer):
    """Сериализатор для ингридиентов"""

    class Meta:
        """Поля и модель для сериализатора Ingredient"""

        model = Ingredient
        fields = '__all__'


#         fields = (
#            'id',
#            'name',
#            'measurement_unit'
#        )
#        read_only_fields = ('__all__',)


class TagSerializer(serializers.ModelSerializer):
    """Сериализатор для тэгов"""

    class Meta:
        """Поля и модель для сериализатора Tag"""

        model = Tag
        fields = '__all__'


# TODO заменить поля на эти, когда доработаю color validator
#       fields = (
#           'id',
#           'name',
#           'color',
#           'slug',
#       )


class RecipeSerializer(serializers.ModelSerializer):
    """Сериализатор для рецептов"""

    class Meta:
        """Поля и модель для рецептов"""

        model = Recipe
        fields = '__all__'
