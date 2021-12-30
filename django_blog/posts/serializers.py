from rest_framework import serializers

from .models import Post
from common.serializers import DisableUpdateUserMixin

from taggit.serializers import TagListSerializerField, TaggitSerializer


class PostSerializer(TaggitSerializer, DisableUpdateUserMixin, serializers.ModelSerializer):
    tags = TagListSerializerField()

    class Meta:
        model = Post
        fields = '__all__'