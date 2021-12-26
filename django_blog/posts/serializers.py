from rest_framework import serializers

from .models import Post

from taggit.serializers import TagListSerializerField, TaggitSerializer


class PostSerializer(TaggitSerializer, serializers.ModelSerializer):
    tags = TagListSerializerField()

    class Meta:
        model = Post
        fields = '__all__'
        read_only_fields = ['user']
