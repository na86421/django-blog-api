from django.contrib.auth import get_user_model

from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        User = get_user_model()
        model = User
        fields = ['id', 'username', 'name', 'created_at', 'modified_at', 'is_staff', 'is_superuser']
