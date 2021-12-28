from rest_framework import serializers

from .models import Comment


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'

    def update(self, instance, validated_data):
        if instance.user != validated_data.get('user', instance.user):
            raise serializers.ValidationError("You cannot change users.")
        return super().update(instance, validated_data)
