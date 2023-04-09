"""API сериализаторы для всех моделей"""
from djoser.serializers import UserCreateSerializer, UserSerializer
from recipes.models import Ingredient, Recipe, Tag, RecipeIngredient
from rest_framework import serializers
from users.models import User
from django.core.exceptions import ValidationError


class CustomUserSerializer(UserSerializer):
    """Сериализатор для модели User"""
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        """Поля и модель сериализатора"""

        model = User
        fields = (
            'email',
            'id',  # TODO это поле возможно надо удалить
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
        )


# TODO: Дописать функцию
#    def get_is_subscribed(self, obj):
#        request = self.context['request'].user
#        if request.is_authenticated and request.following.filter(id=obj.id).exists():
#            return True
#        return False

class CustomUserCreateSerializer(UserCreateSerializer):
    """Сериализатор для создания пользователя"""

    class Meta:
        """Поля и модель для сериализатора CreateUser"""

        model = User
        fields = (
            'email',
            'username',
            'first_name',
            'last_name',
            'password',
        )
        extra_kwargs = {'password': {'write_only': True}}


# TODO: довести до ума проверку
# def validate_username(self, value):
#     if value.lower == 'me':
#         raise ValidationError(
#     'Использовать имя "me" в качестве "username" запрещено')
#     if not re.match(r'^[\w.@+-]+$', value):
#         raise ValidationError('Недопустимое имя пользователя')
#     return value


# def create(self, validated_data):
#     user = MyUser.objects.create(
#         username=validated_data.get('username'),
#         email=validated_data.get('email'),
#         first_name=validated_data.get('first_name'),
#         last_name=validated_data.get('last_name')
#     )
#     user.set_password(validated_data.get('password'))
#     user.save()
#     return user


class IngredientSerializer(serializers.ModelSerializer):
    """Сериализатор для ингридиентов"""

    class Meta:
        """Поля и модель для сериализатора Ingredient"""

        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')


class TagSerializer(serializers.ModelSerializer):
    """Сериализатор для тэгов"""

    # TODO: дописать проверку на цвет
    # color = serializers.CharField(
    #     validators=[color_validator]
    # )

    class Meta:
        """Поля и модель для сериализатора Tag"""

        model = Tag
        fields = (
            'id',
            'name',
            'color',
            'slug',
        )


class RecipeIngredientSerializer(serializers.ModelSerializer):
    """Сериализатор модели RecipeIngredient"""

    pass


class IngredientCreateSerializer(serializers.ModelSerializer):
    """Для ингредиентов при создании рецепта"""
    ingredient = serializers.PrimaryKeyRelatedField(
        queryset=Ingredient.objects.all()
    )

    class Meta:
        model = RecipeIngredient
        fields = ('ingredient', 'amount')


class RecipeSerializer(serializers.ModelSerializer):
    """Сериализатор для получения списка рецептов"""

    class Meta:
        """Поля и модель для рецептов"""

        model = Recipe
        fields = '__all__'


class RecipeCreateSerializer(serializers.ModelSerializer):
    """Сериализатор для создания рецепта"""

    # Для сохранения ингредиентов и тегов рецепта потребуется переопределить методы create и update в ModelSerializer.

    ingredients = IngredientSerializer(
        many=True,
        #     queryset=Ingredient.objects.all()
    )
    tags = TagSerializer(
        many=True,
        #    queryset=Tag.objects.all()
    )

    class Meta:
        """Поля и модель для сериализатора CreateRecipe"""

        model = Recipe
        fields = '__all__'

        def create(self, validated_data):
            """Создание рецепта"""
            ingredients = validated_data.pop('ingredients')
            tags = validated_data.pop('tags')

            recipe = Recipe.objects.create(**validated_data)
            recipe.ingredients.set(ingredients)
            recipe.tags.set(tags)

            return recipe

        # def update(self, instance, validated_data):
        #     """Обновление рецепта"""
        #     ingredients = validated_data.pop('ingredients', instance.ingredients.all())
        #     tags = validated_data.pop('tags', instance.tags.all())
        #
        #     instance.ingredients.set(ingredients)
        #     instance.tags.set(tags)
        #
        #     return super().update(instance, validated_data)

        # Для создания рецепта вместо ответа подставим сериализатор GET

# При создании рецепта вместо ответа подставим сериализатор GET
#    def to_representation(self, instance):
#        serializer = RecipeSerializer(
#            instance,
#            context={'request': self.context.get('request')}
#        )
#
#        return serializer.data
# При публикации рецепта фронтенд кодирует картинку в строку base64; на бэкенде её необходимо декодировать и сохранить как файл.
# Для этого будет удобно создать кастомный тип поля для картинки, переопределив метод сериализатора to_internal_value.
# def get_serializer_class(self):
#    method = self.request.method
#    if method == 'POST':
#        return CompanyCreateSerializer
#    if method == 'PATCH':
#        return CompanyUpdateSerializer
#    if method == 'GET':
#        return CompanyReadSerializer
