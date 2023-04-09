"""Вьюсет для приложения API"""
# from django_filters.rest_framework import DjangoFilterBackend
from djoser.views import UserViewSet
from recipes.models import Ingredient, Recipe, Tag
from rest_framework import viewsets
from users.models import User

# from rest_framework import filters, permissions
from .serializers import (CustomUserSerializer, IngredientSerializer,
                          RecipeCreateSerializer, TagSerializer)


class UsersViewSet(UserViewSet):
    """ViewSet для модели UsersViewSet"""

    queryset = User.objects.all()  # TODO: убрать это поле?


#    serializer_class = CustomUserSerializer  # TODO: убрать это поле?


#   permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class IngredientViewSet(viewsets.ModelViewSet):
    """ViewSet для модели IngredientViewSet"""

    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer


# TODO Сделать пермишены, фильтры, поисковик и пагинацию.
# Указываем фильтрующий бэкенд DjangoFilterBackend
# Из библиотеки django-filter
#  filter_backends = (DjangoFilterBackend, filters.SearchFilter)
# Временно отключим пагинацию на уровне вьюсета,
# так будет удобнее настраивать фильтрацию
# pagination_class = None
# Фильтровать будем по полю name
# filterset_fields = 'name'
# Поиск по имени
# search_fields = ('^name',)


class TagViewSet(viewsets.ModelViewSet):
    """ViewSet для модели TagViewSet"""

    queryset = Tag.objects.all()
    serializer_class = TagSerializer


# TODO Сделать пагинацию и пермишены


class RecipeViewSet(viewsets.ModelViewSet):
    """Viewset для объектов модели RecipeViewSet"""

    queryset = Recipe.objects.all()
    serializer_class = RecipeCreateSerializer


# TODO Сделать пермишены и возможно фильтры
# Добавить / удалить рецепт в список покупок
# Скачать список покупок
# Добавить/Удалить рецепт в/из избранное
# Определяем какой сериализатор использовать. POST, DELETE, GEt
