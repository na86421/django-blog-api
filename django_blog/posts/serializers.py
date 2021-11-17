from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import Post


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
