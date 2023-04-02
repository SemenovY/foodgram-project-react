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
    path('', include('djoser.urls')),
    # TODO Сделать пути для подписок, избранное, список покупок
    #    path(r'.../subscribe/')
    #    path(r'.../favorite/')
    #    path(r'/shopping_cart/')
]
