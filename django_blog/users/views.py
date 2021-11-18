from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, generics, permissions
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import UserSerializer


User = get_user_model()


class SignUpView(APIView):
    permission_classes = [permissions.AllowAny]

    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'username': openapi.Schema(type=openapi.TYPE_STRING, description='username'),
            'name': openapi.Schema(type=openapi.TYPE_STRING, description='name'),
            'password1': openapi.Schema(type=openapi.TYPE_STRING, description='password1, minLength:8'),
            'password2': openapi.Schema(type=openapi.TYPE_STRING, description='password2 confirm, minLength:8'),
        }))
    def post(self, request, format=None):
        data = request.data

        try:
            if data['password1'] != data['password2']:
                return Response({'msg': '비밀번호가 일치하지 않습니다.'}, status=status.HTTP_400_BAD_REQUEST)
            validate_password(data['password1'])

            if User.objects.filter(username=data['username']).exists():
                return Response({'msg': '이미 존재하는 username 입니다.'}, status=status.HTTP_400_BAD_REQUEST)

            user = User.objects.create_user(
                username=data['username'],
                name=data['name'],
                password=data['password1']
            )
            token = Token.objects.create(user=user)

            user_data = {'token': token.key}
            user_data.update(UserSerializer(user).data)
        except KeyError:
            return Response({'msg': '필수 입력항목을 입력해주세요.'}, status=status.HTTP_400_BAD_REQUEST)
        except ValidationError:
            return Response({'msg': '비밀번호를 수정해주세요.'}, status=status.HTTP_400_BAD_REQUEST)

        return Response(user_data, status=status.HTTP_201_CREATED)


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
    UserView can only can only retrieve and update.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
