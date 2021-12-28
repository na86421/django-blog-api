from rest_framework import serializers

from .models import Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

    def validate_name(self, value):
        """
        Check for duplicate category names
        """
        if Category.objects.filter(name=value).exists():
            raise serializers.ValidationError("This is a category name that already exists.")

        return value

    def update(self, instance, validated_data):
        if instance.user != validated_data.get('user', instance.user):
            raise serializers.ValidationError("You cannot change users.")
        return super().update(instance, validated_data)
