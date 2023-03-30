"""Users app serializers."""
from django.contrib.auth import get_user_model
from djoser.serializers import UserCreateSerializer, UserSerializer

User = get_user_model()


class CustomUserSerializer(UserSerializer):
    """User serializer."""

    class Meta:
        """User serializer meta."""

        model = User
        fields = (
            'id',
            'username',
            'email',
            'first_name',
            'last_name',
        )


class CustomUserCreateSerializer(UserCreateSerializer):
    """Сериализатор создания пользователя"""

    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'first_name',
            'last_name',
            'email',
            'password',
        )
