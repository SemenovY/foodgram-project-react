"""Users app urls."""
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import UsersViewSet

app_name = 'api'

router = DefaultRouter()
router.register(r'users', UsersViewSet, basename='users')

urlpatterns = [
    path('', include(router.urls)),
    path(r'auth/', include('djoser.urls.authtoken')),
    #    path('', include('djoser.urls')),
]
