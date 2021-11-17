from django.contrib import admin
from django.contrib.auth import get_user_model

from users.models import Category, Post

# Register your models here.
User = get_user_model()
admin.site.register(User)
admin.site.register(Category)
admin.site.register(Post)
