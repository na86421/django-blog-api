from django.contrib.auth import get_user_model

from rest_framework import serializers

from blog.models import Category, Post 

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        User = get_user_model()
        model = User
        exclude = ['password']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'