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
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            #            'is_subscribed',
        )


class CustomUserCreateSerializer(UserCreateSerializer):
    """Сериализатор создания пользователя"""

    class Meta:
        """CustomUser serializer meta."""

        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'password',
        )
