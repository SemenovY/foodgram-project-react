"""Users app urls."""
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import UserViewSet

app_name = 'users'

router = DefaultRouter()
router.register('users', UserViewSet, basename='users')

urlpatterns = [
    path('', include(router.urls)),
    path(r'auth/', include('djoser.urls')),  # Работа с пользователями.
    path(r'auth/', include('djoser.urls.authtoken')),  # Работа с токенами.,
]
