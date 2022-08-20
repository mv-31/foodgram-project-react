from djoser.serializers import UserSerializer
from rest_framework import serializers

from .models import Follow, CustomUser


class CustomUserCreateSerializer(UserSerializer):
    """
    Сериализатор для создания пользователей.
    """
    class Meta:
        fields = (
            "email",
            "id",
            "username",
            "first_name",
            "last_name",
            "password",
        )
        model = CustomUser


class CustomUserSerializer(UserSerializer):
    """
    Сериализатор для отображения пользователей.
    """
    is_subscribed = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = CustomUser
        fields = (
            "email",
            "id",
            "username",
            "first_name",
            "last_name",
            'is_subscribed',
        )

    def get_is_subscribed(self, obj):
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return Follow.objects.filter(
            author=obj.id, user=user).exists()
