from django.contrib.auth import get_user_model, authenticate

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, generics, permissions
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import UserSerializer


User = get_user_model()


class SignUpView(generics.CreateAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = UserSerializer


class SignInView(APIView):
    permission_classes = [permissions.AllowAny]

    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'username': openapi.Schema(type=openapi.TYPE_STRING, description='username'),
            'password': openapi.Schema(type=openapi.TYPE_STRING, description='password'),
        }))
    def post(self, request, format=None):
        data = request.data

        try:
            user = authenticate(username=data['username'], password=data['password'])
            if user is None:
                return Response({'msg': '로그인에 실패하였습니다.'}, status=status.HTTP_401_UNAUTHORIZED)

            token = Token.objects.get(user=user)

            user_data = {'token': token.key}
            user_data.update(UserSerializer(user).data)
            return Response(user_data)

        except KeyError:
            return Response({'msg': '필수 입력항목을 입력해주세요.'}, status=status.HTTP_400_BAD_REQUEST)


class UserView(generics.RetrieveUpdateAPIView):
    """
    UserView can only retrieve and update.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
