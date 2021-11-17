from django.db import models
from django.contrib.auth import get_user_model

from users.models import Timestampable


class Category(Timestampable):
    name = models.CharField(max_length=200, help_text='카테고리명')
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, help_text='카테고리 생성한 사용자')

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return f'{self.user.name}:{self.name}'

    def has_permission(self, user):
        return True if self.user == user else False
