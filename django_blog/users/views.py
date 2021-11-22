from django.contrib.auth import get_user_model

from rest_framework import generics, permissions
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

from .serializers import SignInSerializer, UserSerializer


User = get_user_model()


class SignUpView(generics.CreateAPIView):
    """
    SignUpView can only create user.
    """
    permission_classes = [permissions.AllowAny]
    serializer_class = UserSerializer


class SignInView(generics.GenericAPIView):
    """
    """
    permission_classes = [permissions.AllowAny]
    serializer_class = SignInSerializer

    def post(self, request, format=None):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data

        token = Token.objects.get(user=user)

        user_data = {'token': token.key}
        user_data.update(UserSerializer(user).data)
        return Response(user_data)


class UserView(generics.RetrieveUpdateAPIView):
    """
    UserView can only retrieve and update.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
