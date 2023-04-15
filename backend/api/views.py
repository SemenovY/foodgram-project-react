"""Основная логика проекта"""
from django.contrib.auth import get_user_model
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

from .filters import IngredientSearchFilter, RecipeFilter
from .mixins import CreateDestroyViewSet, ListSubscriptionViewSet
from .paginators import PageLimitPagination
from .permissions import AuthorAdminOrReadOnly, IsAdminOrReadOnly
from .serializers import (
    CreateRecipeSerializer,
    CustomPasswordSerializer,
    CustomUserCreateSerializer,
    CustomUserSerializer,
    FavoriteSerializer,
    GetRecipeSerializer,
    IngredientSerializer,
    ShoppingCartSerializer,
    SubscribeSerializer,
    TagSerializer,
    UserSubscribeSerializer,
)
from .utils import get_shopping_list

User = get_user_model()


class CustomUserViewSet(UserViewSet):
    """ViewSet используется для создания и удаления подписок"""

    pagination_class = PageLimitPagination
    add_serializer = UserSubscribeSerializer

    def get_serializer_class(self):
        if self.action == "create":
            return CustomUserCreateSerializer
        if self.action == "set_password":
            return CustomPasswordSerializer
        return CustomUserSerializer

    def get_permissions(self):
        if self.action == "retrieve":
            self.permission_classes = (IsAuthenticated,)
        return super().get_permissions()

    @action(
        methods=(
            "post",
            "delete",
        ),
        detail=True,
        permission_classes=(IsAuthenticated,),
    )
    def subscribe(self, request, id=None):
        """Подписка и отписка на/от пользователя"""
        user = request.user
        author = get_object_or_404(User, pk=id)
        serializer = SubscribeSerializer(
            data={
                "user": user.id,
                "author": author.id,
            }
        )
        if request.method == "POST":
            serializer.is_valid(raise_exception=True)
            serializer.save()
            serializer_show = UserSubscribeSerializer(
                author,
                context={"recipes_limit": request.GET.get("recipes_limit")},
            )
            return Response(
                serializer_show.data, status=status.HTTP_201_CREATED
            )
        if request.method == "DELETE":
            subscription = Subscriptions.objects.filter(
                user=user, author=author
            )
            if author == user or not subscription.exists():
                return Response(
                    "Вы не можете отписаться от того, на кого не подписаны!",
                    status=status.HTTP_400_BAD_REQUEST,
                )
            subscription.delete()
            return Response(
                "Подписка удалена", status=status.HTTP_204_NO_CONTENT
            )


class SubscriptionViewSet(ListSubscriptionViewSet):
    """Представление списка подписок текущего пользователя"""

    pagination_class = PageLimitPagination
    serializer_class = UserSubscribeSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return User.objects.filter(subscription__user=self.request.user)


class TagViewSet(ReadOnlyModelViewSet):
    """Получение тега или списка всех тегов"""

    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (IsAdminOrReadOnly,)


class IngredientViewSet(ReadOnlyModelViewSet):
    """
    Получение ингредиента или списка всех ингредиентов,
    поиск по частичному вхождению в начале названия ингредиента.
    """

    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (IngredientSearchFilter,)
    search_fields = ("^name",)


class RecipesViewSet(ModelViewSet):
    """Получение, создание и частичное изменение, а так же удаления рецептов.
    Реализована фильтрация по тегам, автору,
    присутствию рецептов в избранном и списке покупок.
    """

    queryset = Recipe.objects.all()
    permissions = (AuthorAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter
    pagination_class = PageLimitPagination

    def get_serializer_class(self):
        method = self.request.method
        if method == "POST" or method == "PATCH":
            return CreateRecipeSerializer
        return GetRecipeSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"request": self.request})
        return context

    @action(
        detail=False,
        methods=["GET"],
        url_path="download_shopping_cart",
        permission_classes=[IsAuthenticated],
    )
    def download_shopping_cart(self, request):
        """Выгрузка текстового файла со списком покупок"""
        user = self.request.user
        if not user.shopping_cart.exists():
            return Response(
                "Вы не добавили ни одного рецепта в корзину.",
                status=status.HTTP_400_BAD_REQUEST,
            )
        return get_shopping_list(self, request)


class FavoriteViewSet(CreateDestroyViewSet):
    """ViewSet для добавления и удаления рецепта в/из избранного"""

    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["recipe_id"] = self.kwargs.get("recipe_id")
        return context

    def perform_create(self, serializer):
        """Добавление рецепта в избранное"""
        serializer.save(
            user=self.request.user,
            favorite_recipe=get_object_or_404(
                Recipe, id=self.kwargs.get("recipe_id")
            ),
        )

    @action(methods=("delete",), detail=True)
    def delete(self, request, recipe_id):
        """Удаление рецепта из избранного"""
        get_object_or_404(
            Favorite, user=request.user, favorite_recipe_id=recipe_id
        ).delete()
        return Response(
            "Рецепт удален из избранного", status=status.HTTP_204_NO_CONTENT
        )


class ShoppingCartViewSet(CreateDestroyViewSet):
    """ViewSet для добавления и удаления рецепта в/из списка покупок"""

    queryset = ShoppingCart.objects.all()
    serializer_class = ShoppingCartSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["recipe_id"] = self.kwargs.get("recipe_id")
        return context

    def perform_create(self, serializer):
        """Добавление рецепта в корзину"""
        serializer.save(
            user=self.request.user,
            recipe=get_object_or_404(Recipe, id=self.kwargs.get("recipe_id")),
        )

    @action(methods=("delete",), detail=True)
    def delete(self, request, recipe_id):
        """Удаление рецепта из корзины"""
        get_object_or_404(
            ShoppingCart, user=request.user, recipe_id=recipe_id
        ).delete()
        return Response(
            "Рецепт удален из корзины", status=status.HTTP_204_NO_CONTENT
        )
