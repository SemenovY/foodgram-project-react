"""Users app urls."""
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

from .views import UserViewSet, get_jwt_token, signup

router_v1 = DefaultRouter()
router_v1.register('users', UserViewSet)

auth_patterns = [
    path('signup/', signup, name='signup'),
    path('token/', get_jwt_token, name='get_jwt_token'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

urlpatterns = [
    path('v1/auth/', include(auth_patterns)),
    path('v1/', include(router_v1.urls)),
]
