"""Все основные урл"""
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (CustomUserViewSet, FavoriteViewSet, IngredientViewSet,
                    RecipesViewSet, ShoppingCartViewSet, SubscriptionViewSet,
                    TagViewSet)

app_name = 'api'

router = DefaultRouter()


router.register('users', CustomUserViewSet, basename='user')
router.register(
    r'users/subscriptions', SubscriptionViewSet, basename='subscriptions'
)
router.register('ingredients', IngredientViewSet, basename='ingredients')
router.register('tags', TagViewSet, basename='tags')
router.register('recipes', RecipesViewSet, basename='recipes')
router.register(
    r'recipes/(?P<recipe_id>\d+)/favorite',
    FavoriteViewSet,
    basename='favorite',
)
router.register(
    r'recipes/(?P<recipe_id>\d+)/shopping_cart',
    ShoppingCartViewSet,
    basename='shopping_cart',
)


urlpatterns = [
    path('', include(router.urls)),
    path('', include('djoser.urls.base')),
    path('auth/', include('djoser.urls.authtoken')),
]
