from rest_framework import serializers

from .models import Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
        read_only_fields = ['user']

    def validate_name(self, value):
        """
        Check for duplicate category names
        """
        if Category.objects.filter(name=value).exists():
            raise serializers.ValidationError("This is a category name that already exists.")

        return value
