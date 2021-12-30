from django.db import models
from django.contrib.auth import get_user_model

from common.models import Timestampable
from categories.models import Category

from taggit.managers import TaggableManager


class Post(Timestampable):
    title = models.CharField(max_length=50, help_text='포스트 제목')
    content = models.CharField(max_length=100, help_text='포스트 내용')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, help_text='속한 카테고리')
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, help_text='포스트 생성한 사용자')
    hits = models.PositiveIntegerField(default=0, help_text='조회수')
    is_notice = models.BooleanField(default=False, help_text='공지사항 여부')
    tags = TaggableManager()

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return f'{self.user.name}:{self.category.name}:{self.title}'

    def increase_hits(self):
        self.hits += 1
        self.save()
