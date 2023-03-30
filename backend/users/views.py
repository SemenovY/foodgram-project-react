"""Users app views."""
from djoser.views import UserViewSet

from .models import User
from .serializers import CustomUserSerializer

# from rest_framework import permissions, viewsets
# from rest_framework.pagination import PageNumberPagination


class UsersViewSet(UserViewSet):
    """ViewSet for users."""

    queryset = User.objects.all()
    serializer_class = CustomUserSerializer


#    pagination_class = PageNumberPagination
#    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
#   permission_classes = (permissions.AllowAny,)
