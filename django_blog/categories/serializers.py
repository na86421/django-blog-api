from rest_framework import serializers

from .models import Category
from common.serializers import DisableUpdateUserMixin


class CategorySerializer(DisableUpdateUserMixin, serializers.ModelSerializer):
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
