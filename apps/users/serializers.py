from .models import CustomUser
from rest_framework import serializers


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'uuid', 'email', 'first_name', 'last_name', 'middle_name', 'username', 'created_at']
