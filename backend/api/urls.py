"""Пути для приложения API"""
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import IngredientViewSet, RecipeViewSet, TagViewSet, UsersViewSet

app_name = 'api'

router = DefaultRouter()

router.register(r'users', UsersViewSet, basename='users')
router.register(r'ingredients', IngredientViewSet, basename='ingredients')
router.register(r'tags', TagViewSet, basename='tags')
router.register(r'recipes', RecipeViewSet, basename='recipes')

urlpatterns = [
    path('', include(router.urls)),
    path(r'auth/', include('djoser.urls.authtoken')),
    path(r'users/<int:id>/subscribe/', UsersViewSet.as_view({
        'post': 'subscribe',
        'delete': 'subscribe'
    }),
         name='subscribe'
         ),
    path(r'recipes/<int:id>/favorite/', RecipeViewSet.as_view({
        'post': 'favorite',
        'delete': 'favorite'
    }),
         name='favorite'
         ),
    path(r'recipes/<int:id>/shopping_cart/', RecipeViewSet.as_view({
        'post': 'shopping_cart',
        'delete': 'shopping_cart'
    }),
         name='shopping_cart'
         ),
]
