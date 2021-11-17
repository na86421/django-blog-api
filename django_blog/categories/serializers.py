from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import Category


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
