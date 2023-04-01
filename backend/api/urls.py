"""API URL Configuration."""
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import IngredientViewSet, UsersViewSet

app_name = 'api'

router = DefaultRouter()
router.register(r'users', UsersViewSet, basename='users')
router.register(r'ingredients', IngredientViewSet, basename='ingredients')

urlpatterns = [
    path('', include(router.urls)),
    path(r'auth/', include('djoser.urls.authtoken')),
    path('', include('djoser.urls')),
]