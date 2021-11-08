from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets, status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from blog.models import Category, Post
from blog.api.serializers import UserSerializer, CategorySerializer, PostSerializer


User = get_user_model()


class SignUpView(APIView):
    permission_classes = [AllowAny]

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
    permission_classes = [AllowAny]

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


class UserViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser]
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action in ['retrieve', 'partial_update']:
            self.permission_classes = [IsAuthenticated]
        return super().get_permissions()

    def update(self, request, *args, **kwargs):
        data = request.data
        user = self.get_object()

        if not user.has_permission(request.user):
            return Response({'msg': '프로필을 수정할 권한이 없습니다.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            validate_password(data['password'])

            user.name = data['name']
            user.set_password(data['password'])
            user.save()
            return Response(UserSerializer(user).data)

        except KeyError:
            return Response({'msg': '필수 입력항목을 입력해주세요.'}, status=status.HTTP_400_BAD_REQUEST)
        except ValidationError:
            return Response({'msg': '비밀번호를 수정해주세요.'}, status=status.HTTP_400_BAD_REQUEST)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def create(self, request, *args, **kwargs):
        data = request.data
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)

        if Category.objects.filter(name=data['name']).exists():
            return Response({'msg': '이미 존재하는 카테고리명 입니다.'}, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def destroy(self, request, pk=None):
        category = self.get_object()

        if not category.has_permission(request.user):
            return Response({'msg': '카테고리를 생성한 유저가 아닙니다.'}, status=status.HTTP_400_BAD_REQUEST)

        category.delete()
        return Response({'msg': '카테고리가 삭제되었습니다.'})

    def update(self, request, *args, **kwargs):
        category = self.get_object()
        data = request.data
        serializer = self.get_serializer(category, data=data, partial=True)
        serializer.is_valid(raise_exception=True)

        if not category.has_permission(request.user):
            return Response({'msg': '카테고리를 생성한 유저가 아닙니다.'}, status=status.HTTP_400_BAD_REQUEST)

        if Category.objects.filter(name=data['name']).exclude(id=category.id).exists():
            return Response({'msg': '이미 존재하는 카테고리명 입니다.'}, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response(serializer.data)


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def retrieve(self, request, *args, **kwargs):
        post = self.get_object()
        post.increase_hits()
        serializer = self.get_serializer(post)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        data = request.data
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)

        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def destroy(self, request, pk=None):
        post = self.get_object()

        if not post.has_permission(request.user):
            return Response({'msg': '포스트를 생성한 유저가 아닙니다.'}, status=status.HTTP_400_BAD_REQUEST)

        post.delete()
        return Response({'msg': '포스트가 삭제되었습니다.'})

    def update(self, request, *args, **kwargs):
        post = self.get_object()
        data = request.data
        serializer = self.get_serializer(post, data=data, partial=True)
        serializer.is_valid(raise_exception=True)

        if not post.has_permission(request.user):
            return Response({'msg': '포스트를 생성한 유저가 아닙니다.'}, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response(serializer.data)
