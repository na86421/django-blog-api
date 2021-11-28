from django.contrib.auth import get_user_model
from django.test import TestCase

from categories.models import Category
from posts.models import Post


class UserTest(TestCase):
    def setUp(self):
        print(f'-------{self._testMethodName}-------')

    def test_create_user(self):
        user = get_user_model().objects.create_user(username='na66421', name='윤준기', password='qwer!@#$')

        self.assertEqual(user.username, 'na66421')
        self.assertEqual(user.name, '윤준기')
        self.assertEqual(str(user), user.name, '__str__ 불일치')


class CategoryTest(TestCase):
    def setUp(self):
        print(f'-------{self._testMethodName}-------')

    def test_create_category(self):
        user = get_user_model().objects.create_user(username='na66421', name='윤준기', password='qwer!@#$')
        category = Category.objects.create(name='python', user=user)

        self.assertEqual(category.name, 'python')
        self.assertEqual(str(category), f'{user.name}:{category.name}', '__str__ 불일치')


class PostTest(TestCase):
    def setUp(self):
        print(f'-------{self._testMethodName}-------')

    def test_create_post(self):
        user = get_user_model().objects.create_user(username='na66421', name='윤준기', password='qwer!@#$')
        category = Category.objects.create(name='python', user=user)
        post = Post.objects.create(title='title', content='content', category=category, user=user)

        self.assertEqual(post.title, 'title')
        self.assertEqual(str(post), f'{user.name}:{category.name}:{post.title}', '__str__ 불일치')

    def test_post_increase_hits(self):
        user = get_user_model().objects.create(email='na66421@gmail.com', username='na66421',
                                               name='윤준기', password='qwer1234')
        category = Category.objects.create(name='프로그래밍', user=user)
        post = Post.objects.create(title='title', content='content', category=category, user=user)

        before_hits = post.hits
        post.increase_hits()
        self.assertEqual(before_hits + 1, post.hits)
