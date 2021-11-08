from django.contrib.auth import get_user_model

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

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

    def validate(self, data):
        '''
        check name field is required
        '''
        err_msg = {"name": ["This field is required."]}
        if 'name' not in data:
            raise ValidationError(err_msg)
        return data


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'

    def validate(self, data):
        '''
        check title, content, category field is required
        '''
        err_msg = {}
        if 'title' not in data:
            err_msg['title'] = ["This field is required."]
        if 'content' not in data:
            err_msg['content'] = ["This field is required."]
        if 'category' not in data:
            err_msg['category'] = ["This field is required."]
        if bool(err_msg) is not False:
            raise ValidationError(err_msg)
        return data
