from django.db import models
from django.contrib.auth.models import AbstractUser


class Timestampable(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    class Meta:
        abstract = True


class User(AbstractUser, Timestampable):
    name = models.CharField(max_length=200, help_text='사용자 이름')

    def __str__(self):
        return self.name


class Category(Timestampable):
    name = models.CharField(max_length=200, help_text='카테고리명')
    user = models.ForeignKey(User, on_delete=models.CASCADE, help_text='카테고리 생성한 사용자')

    def __str__(self):
        return f'{self.user.name}:{self.name}'

    def has_permission(self, user):
        return True if self.user == user else False

class Post(Timestampable):
    title = models.CharField(max_length=50, help_text='포스트 제목')
    content = models.CharField(max_length=100, help_text='포스트 내용')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, help_text='속한 카테고리')
    user = models.ForeignKey(User, on_delete=models.CASCADE, help_text='포스트 생성한 사용자')

    def __str__(self):
        return f'{self.user.name}:{self.category.name}:{self.title}'

    def has_permission(self, user):
        return True if self.user == user else False
