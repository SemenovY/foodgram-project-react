"""API app views."""
from django_filters.rest_framework import DjangoFilterBackend
from djoser.views import UserViewSet
from recipes.models import Ingredient
from rest_framework import filters, viewsets
from users.models import User

from .serializers import CustomUserSerializer, IngredientSerializer


class UsersViewSet(UserViewSet):
    """ViewSet для модели пользователь."""

    queryset = User.objects.all()  # убрать это поле
    serializer_class = CustomUserSerializer  # убрать это поле


class IngredientViewSet(viewsets.ModelViewSet):
    """ViewSet для модели ингредиентов."""

    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
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
