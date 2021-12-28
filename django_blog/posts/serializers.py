from rest_framework import serializers

from .models import Post

from taggit.serializers import TagListSerializerField, TaggitSerializer


class PostSerializer(TaggitSerializer, serializers.ModelSerializer):
    tags = TagListSerializerField()

    class Meta:
        model = Post
        fields = '__all__'

    def update(self, instance, validated_data):
        if instance.user != validated_data.get('user', instance.user):
            raise serializers.ValidationError("You cannot change users.")
        return super().update(instance, validated_data)
