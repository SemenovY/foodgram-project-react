"""Users app views."""
from rest_framework import viewsets

from .models import User
from .serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    """ViewSet for users."""

    queryset = User.objects.all()
    serializer_class = UserSerializer
