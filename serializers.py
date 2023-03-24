"""Users app serializers."""
from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):
    """User serializer."""

    class Meta:
        """User serializer meta."""

        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'password',
        )
