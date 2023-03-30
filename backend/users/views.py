"""Users app views."""
from rest_framework import permissions, viewsets
from rest_framework.pagination import PageNumberPagination

from .models import User
from .serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    """ViewSet for users."""

    queryset = User.objects.all()
    #    serializer_class = UserSerializer
    pagination_class = PageNumberPagination
    #    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    permission_classes = (permissions.AllowAny,)
