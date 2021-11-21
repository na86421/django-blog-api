from django.contrib.auth import get_user_model, password_validation

from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = get_user_model()
        fields = ['id', 'username', 'name', 'created_at', 'modified_at', 'is_staff', 'is_superuser', 'password']

    def validate_password(self, value):
        """
        Check that the password is not simple.
        """
        password_validation.validate_password(value)
        return value


# TODO
class SignInSerializer(serializers.Serializer):
    pass
