from django.contrib.auth import authenticate, get_user_model, password_validation

from rest_framework import serializers, exceptions


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = get_user_model()
        fields = ['id', 'username', 'name', 'created_at', 'modified_at', 'is_staff', 'is_superuser', 'password']

    def create(self, validated_data):
        user = get_user_model().objects.create_user(
            username=validated_data['username'],
            name=validated_data['name'],
            password=validated_data['password'],
        )

        return user

    def validate_password(self, value):
        """
        Check that the password is not simple.
        """
        password_validation.validate_password(value)
        return value


class SignInSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

    def validate(self, attrs):
        user = authenticate(**attrs)
        if user is None:
            raise exceptions.AuthenticationFailed
        return user
