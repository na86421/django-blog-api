from django.db import models
from django.contrib.auth.models import AbstractUser


class Timestampable(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    class Meta:
        abstract = True


class User(AbstractUser, Timestampable):
    name = models.CharField(max_length=200, blank=True, help_text='사용자 이름')

    def __str__(self):
        return self.name
