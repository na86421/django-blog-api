from unittest import mock

from django.contrib.auth import get_user_model
from django.test import TestCase

from categories.models import Category
from posts.models import Post


class PostTest(TestCase):
    def setUp(self):
        print(f'-------{self._testMethodName}-------')

    def test_post_increase_hits(self):
        user = get_user_model().objects.create(email='na66421@gmail.com', username='na66421',
                                               name='윤준기', password='qwer1234')
        category = Category.objects.create(name='프로그래밍', user=user)
        post = Post.objects.create(title='title', content='content', category=category, user=user)

        before_hits = post.hits
        post.increase_hits()
        self.assertEqual(before_hits + 1, post.hits)
