from django.db import models
from django.contrib.auth import get_user_model

from users.models import Timestampable
from posts.models import Post


class Comment(Timestampable):
    content = models.CharField(max_length=100, help_text='댓글 내용')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, help_text='속한 포스트')
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, editable=False, help_text='댓글 단 사용자')

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return f'{self.user.name}:{self.post.title}:{self.content}'
