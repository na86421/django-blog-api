from django.contrib.auth import get_user_model

from rest_framework import viewsets

from blog.models import Category, Post
from blog.api.serializers import UserSerializer, CategorySerializer, PostSerializer

class UserViewSet(viewsets.ModelViewSet):
    User = get_user_model()
    queryset = User.objects.all()
    serializer_class = UserSerializer

    # def create(self, request):
    #     user = User.objects.create


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    