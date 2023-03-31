"""Users app views."""
from djoser.views import UserViewSet
from users.models import User

from .serializers import CustomUserSerializer


class UsersViewSet(UserViewSet):
    """ViewSet for users."""

    queryset = User.objects.all()
    serializer_class = CustomUserSerializer
