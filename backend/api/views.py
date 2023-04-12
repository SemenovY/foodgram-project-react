from datetime import datetime as dt

from django.contrib.auth import get_user_model
from django.db.models import F, Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from djoser.views import UserViewSet
from recipes.models import Favorite, Ingredient, Recipe, ShoppingCart, Tag
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from users.models import Subscriptions

from backend.settings import DATE_TIME_FORMAT

from .filters import IngredientSearchFilter, RecipeFilter
from .mixins import CreateDestroyViewSet, ListSubscriptionViewSet
from .paginators import PageLimitPagination
from .permissions import AuthorAdminOrReadOnly, IsAdminOrReadOnly
from .serializers import (CreateRecipeSerializer, CustomPasswordSerializer,
                          CustomUserCreateSerializer, CustomUserSerializer,
                          FavoriteSerializer, GetRecipeSerializer,
                          IngredientSerializer, ShoppingCartSerializer,
                          SubscribeSerializer, TagSerializer,
                          UserSubscribeSerializer)

User = get_user_model()


class CustomUserViewSet(UserViewSet):
    """Кастомый вьюсет для пользователей,
    также используется для создания и удаления подписок."""

    pagination_class = PageLimitPagination
    add_serializer = UserSubscribeSerializer

    def get_serializer_class(self):
        if self.action == 'create':
            return CustomUserCreateSerializer
        if self.action == 'set_password':
            return CustomPasswordSerializer
        return CustomUserSerializer

    def get_permissions(self):
        if self.action == 'retrieve':
            self.permission_classes = (IsAuthenticated,)
        return super().get_permissions()

    @action(
        methods=(
            'post',
            'delete',
        ),
        detail=True,
        permission_classes=(IsAuthenticated,),
    )
    def subscribe(self, request, id=None):
        """Подписка и отписка на/от пользователя."""
        user = request.user
        author = get_object_or_404(User, pk=id)
        serializer = SubscribeSerializer(
            data={
                'user': user.id,
                'author': author.id,
            }
        )
        if request.method == 'POST':
            serializer.is_valid(raise_exception=True)
            serializer.save()
            serializer_show = UserSubscribeSerializer(
                author,
                context={'recipes_limit': request.GET.get('recipes_limit')},
            )
            return Response(
                serializer_show.data, status=status.HTTP_201_CREATED
            )
        if request.method == 'DELETE':
            subscription = Subscriptions.objects.filter(
                user=user, author=author
            )
            if author == user or not subscription.exists():
                return Response(
                    'Вы не можете отписаться от того, на кого не подписаны!',
                    status=status.HTTP_400_BAD_REQUEST,
                )
            subscription.delete()
            return Response(
                'Подписка удалена', status=status.HTTP_204_NO_CONTENT
            )


class SubscriptionViewSet(ListSubscriptionViewSet):
    """Класс представления списка подписок текущего пользователя."""

    pagination_class = PageLimitPagination
    serializer_class = UserSubscribeSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return User.objects.filter(subscription__user=self.request.user)


class TagViewSet(ReadOnlyModelViewSet):
    """Вьюсет получения тега или списка всех тегов.
    Доступ на изменение только администратору.
    """

    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (IsAdminOrReadOnly,)


class IngredientViewSet(ReadOnlyModelViewSet):
    """Вьюсет полчения ингредиента или списка всех ингредиентов.
    Доступ на изменение только администратору.
    Добавлен поиск по частичному вхождению в начале названия ингредиента.
    """

    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (IngredientSearchFilter,)
    search_fields = ('^name',)


class RecipesViewSet(ModelViewSet):
    """Вьюсет для получения, создания,частичного изменения
    и удаления рецептов. Реализована фильтрация по тегам, автору,
    присутсвию рецептов в избранном и списке покупок.
    """

    queryset = Recipe.objects.all()
    permissions = (AuthorAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter
    pagination_class = PageLimitPagination

    def get_serializer_class(self):
        method = self.request.method
        if method == 'POST' or method == 'PATCH':
            return CreateRecipeSerializer
        return GetRecipeSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({'request': self.request})
        return context

    @action(methods=('get',), detail=False)
    def download_shopping_cart(self, request):
        """Выгрузка файла .txt со списком покупок
        Подсчет суммы ингредиентов по всем рецептам из корзины
        Адрес: */recipes/download_shopping_cart/.
        """
        user = self.request.user
        if not user.shopping_cart.exists():
            return Response(
                'Вы не добавили ни обного рецепта в корзину.',
                status=status.HTTP_400_BAD_REQUEST,
            )

        filename = f'{user.username}_shopping_list.txt'
        shopping_list = [
            f'Список покупок пользователя:\n'
            f'{user.first_name} {user.last_name}\n'
            f'Дата: {dt.now().strftime(DATE_TIME_FORMAT)}\n'
            f'____________________________'
        ]

        ingredients = (
            Ingredient.objects.filter(
                amount__recipe__shopping_cart_recipe__user=user
            )
            .values('name', measurement=F('measurement_unit'))
            .annotate(amount=Sum('amount__amount'))
        )

        for ing in ingredients:
            shopping_list.append(
                f'- {ing["name"]}: {ing["amount"]} {ing["measurement"]}'
            )

        shopping_list.append(
            '____________________________\n'
            'Вперед за покупками!\n'
            'Спасибо, что пользуететсь Foodgram'
        )
        shopping_list = '\n'.join(shopping_list)
        response = HttpResponse(
            shopping_list, content_type='text.txt; charset=utf-8'
        )
        response['Content-Disposition'] = f'attachment; filename={filename}'
        return response


class FavoriteViewSet(CreateDestroyViewSet):
    """Вьюсет для добавления и удаления рецепта в/из избранного."""

    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['recipe_id'] = self.kwargs.get('recipe_id')
        return context

    def perform_create(self, serializer):
        serializer.save(
            user=self.request.user,
            favorite_recipe=get_object_or_404(
                Recipe, id=self.kwargs.get('recipe_id')
            ),
        )

    @action(methods=('delete',), detail=True)
    def delete(self, request, recipe_id):
        get_object_or_404(
            Favorite, user=request.user, favorite_recipe_id=recipe_id
        ).delete()
        return Response(
            'Рецепт удален из избранного', status=status.HTTP_204_NO_CONTENT
        )


class ShoppingCartViewSet(CreateDestroyViewSet):
    """Вьюсет для добавления и удаления рецепта в/из списка покупок."""

    queryset = ShoppingCart.objects.all()
    serializer_class = ShoppingCartSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['recipe_id'] = self.kwargs.get('recipe_id')
        return context

    def perform_create(self, serializer):
        serializer.save(
            user=self.request.user,
            recipe=get_object_or_404(Recipe, id=self.kwargs.get('recipe_id')),
        )

    @action(methods=('delete',), detail=True)
    def delete(self, request, recipe_id):
        get_object_or_404(
            ShoppingCart, user=request.user, recipe_id=recipe_id
        ).delete()
        return Response(
            'Рецепт удален из корзины', status=status.HTTP_204_NO_CONTENT
        )
