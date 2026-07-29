from rest_framework import serializers
from .models import CustomUser


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'role', 'phone')
        read_only_fields = ('id',)


class UserMeSerializer(serializers.ModelSerializer):
    """Joriy foydalanuvchi profili uchun serializer."""

    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'role', 'phone', 'is_staff')
        read_only_fields = ('id', 'username', 'is_staff', 'role')
