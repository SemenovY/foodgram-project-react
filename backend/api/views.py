"""Вьюсет для приложения API"""
# from django.contrib.auth import get_user_model
from djoser.views import UserViewSet
from recipes.models import Ingredient, Recipe, Tag
from rest_framework import permissions, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .filters import IngredientFilter, RecipeFilterBackend
from .pagination import CustomPageNumberPagination
from .permissions import IsAuthorOrReadOnly
from .serializers import (
    CreateRecipeSerializer,
    IngredientSerializer,
    RecipeSerializer,
    TagSerializer,
)

# TODO возможно нужно удалить эту переменную юзер
# User = get_user_model()


class UsersViewSet(UserViewSet):
    """ViewSet для модели Users"""

    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    pagination_class = CustomPageNumberPagination

    # @action(
    #     methods=['GET'],
    #     detail=False,
    #     url_path='subscriptions',
    #     url_name='subscriptions',
    #     permission_classes=[IsAuthenticated, ]
    #     )
    #
    # def subscriptions(self, request):
    #     """Выдает авторов, на кого подписан пользователь"""
    #     user = request.user
    #     queryset = MyUser.objects.filter(following__user=user)
    #     pages = self.paginate_queryset(queryset)
    #     serializer = UserFollowSerializer(
    #         pages, many=True, context={'request': request}
    #     )
    #     return self.get_paginated_response(serializer.data)
    #
    # @action(
    #     methods=['POST', 'DELETE'],
    #     detail=True,
    #     url_path='subscribe',
    #     url_name='subscribe',
    #     permission_classes=[IsAuthenticated, ])
    #
    # def subscribe(self, request, id=None):
    #     """Подписаться/отписаться на/от автора"""
    #     user = self.request.user
    #     author = get_object_or_404(MyUser, pk=id)
    #
    #     if self.request.method == 'POST':
    #         if user == author:
    #             raise exceptions.ValidationError(
    #                 'Подписка на самого себя запрещена.'
    #             )
    #         if Follow.objects.filter(
    #             user=user,
    #             author=author
    #         ).exists():
    #             raise exceptions.ValidationError('Подписка уже оформлена.')
    #
    #         Follow.objects.create(user=user, author=author)
    #         serializer = self.get_serializer(author)
    #
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #
    #     if self.request.method == 'DELETE':
    #         if not Follow.objects.filter(
    #             user=user,
    #             author=author
    #         ).exists():
    #             raise exceptions.ValidationError(
    #                 'Подписка не была оформлена, либо уже удалена.'
    #             )
    #         subscription = get_object_or_404(
    #             Follow,
    #             user=user,
    #             author=author
    #         )
    #         subscription.delete()
    #         return Response(status=status.HTTP_204_NO_CONTENT)
    #     return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


class IngredientViewSet(viewsets.ModelViewSet):
    """ViewSet для модели Ingredient"""

    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filterset_class = IngredientFilter
    search_fields = ('^name',)
    pagination_class = None


class TagViewSet(viewsets.ModelViewSet):
    """ViewSet для модели Tag"""

    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class RecipeViewSet(viewsets.ModelViewSet):
    """Viewset для модели Recipe"""

    queryset = Recipe.objects.all()
    permission_classes = (IsAuthorOrReadOnly,)
    filter_backends = [RecipeFilterBackend]
    pagination_class = CustomPageNumberPagination

    def get_serializer_class(self):
        """Выбор сериализатора между Post/Update or GET"""

        if self.action in ('create', 'partial_update'):
            return CreateRecipeSerializer

        return RecipeSerializer

    @action(
        methods=[
            'POST',
        ],
        detail=False,
        url_path='recipes',
        url_name='recipes',
        permission_classes=[
            IsAuthenticated,
        ],
    )
    def recipes(self, request):
        serializer = RecipeSerializer(
            data=request.data, context={'author': request.user}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )

    @action(
        methods=[
            'DELETE',
        ],
        detail=False,
        url_path='recipes',
        url_name='recipes',
        permission_classes=[
            IsAuthenticated,
        ],
    )
    def recipes_delete(self, request):
        recipe_id = request.query_params.get('id')
        if not recipe_id:
            return Response(
                {'detail': 'Не указан идентификатор рецепта'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            recipe = Recipe.objects.get(id=recipe_id)
        except Recipe.DoesNotExist:
            return Response(
                {'detail': 'Рецепт не найден'},
                status=status.HTTP_404_NOT_FOUND,
            )
        if recipe.author != request.user:
            return Response(
                {'detail': 'Вы не можете удалять чужой рецепт'},
                status=status.HTTP_403_FORBIDDEN,
            )
        recipe.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
