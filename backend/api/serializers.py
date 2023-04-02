"""API сериализаторы для всех моделей"""
from django.contrib.auth import get_user_model
from djoser.serializers import UserCreateSerializer, UserSerializer
from recipes.models import Ingredient, Tag
from rest_framework import serializers

User = get_user_model()


class CustomUserSerializer(UserSerializer):
    """Сериализатор для модели User"""

    class Meta:
        """Поля и модель сериализатора"""

        model = User
        fields = (
            'email',
            'id',
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
            'id',
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
        read_only_fields = ('__all__',)


class TagSerializer(serializers.ModelSerializer):
    """Сериализатор для тэгов"""

    class Meta:
        """Поля и модель для сериализатора Tag"""

        model = Tag
        fields = '__all__'
