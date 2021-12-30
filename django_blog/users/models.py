from django.db import models
from django.contrib.auth.models import AbstractUser

from common.models import Timestampable


class User(AbstractUser, Timestampable):
    name = models.CharField(max_length=200, help_text='사용자 이름')

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.name
