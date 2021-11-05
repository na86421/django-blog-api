from unittest import mock

from django.contrib.auth import get_user_model
from django.utils import timezone
from django.test import TestCase

from blog.models import Category, Post


User = get_user_model()


class UserModelTest(TestCase):
    def setUp(self):
        print(f'-------{self._testMethodName}-------')

    def test_create_user(self):
        mock_date = timezone.now()
        with mock.patch('django.utils.timezone.now') as mock_now:
            mock_now.return_value = mock_date
            user = User.objects.create(email='na66421@gmail.com', username='na66421',
                                       name='윤준기', password='qwer1234')

        self.assertEqual(user.email, 'na66421@gmail.com', 'email 불일치')
        self.assertEqual(user.username, 'na66421', 'username 불일치')
        self.assertEqual(user.name, '윤준기', 'name 불일치')
        self.assertEqual(user.password, 'qwer1234', 'password 불일치')
        self.assertEqual(user.created_at, mock_date, '생성시간 불일치')
        self.assertEqual(user.modified_at, mock_date, '수정시간 불일치')
        self.assertEqual(str(user), user.name, '__str__ 불일치')

    def test_has_permission(self):
        user = User.objects.create(email='na66421@gmail.com', username='na66421',
                                   name='윤준기', password='qwer1234')
        user2 = User.objects.create(email='na66421_2@gmail.com', username='na66421_2',
                                   name='윤준기2', password='qwer1234')

        category = Category.objects.create(name='프로그래밍', user=user)

        self.assertTrue(category.has_permission(user))
        self.assertFalse(category.has_permission(user2))


class CategoryTest(TestCase):
    def setUp(self):
        print(f'-------{self._testMethodName}-------')

    def test_create_category(self):
        mock_date = timezone.now()
        with mock.patch('django.utils.timezone.now') as mock_now:
            mock_now.return_value = mock_date
            user = User.objects.create(email='na66421@gmail.com', username='na66421',
                                       name='윤준기', password='qwer1234')
            category = Category.objects.create(name='프로그래밍', user=user)

        self.assertEqual(category.name, '프로그래밍', '카테고리 이름 불일치')
        self.assertEqual(category.user, user, '카테고리 생성 사용자 불일치')
        self.assertEqual(category.created_at, mock_date, '생성시간 불일치')
        self.assertEqual(category.modified_at, mock_date, '수정시간 불일치')
        self.assertEqual(str(category), f'{user.name}:{category.name}', '__str__ 불일치')


class PostTest(TestCase):
    def setUp(self):
        print(f'-------{self._testMethodName}-------')

    def test_create_post(self):
        mock_date = timezone.now()
        with mock.patch('django.utils.timezone.now') as mock_now:
            mock_now.return_value = mock_date
            user = User.objects.create(email='na66421@gmail.com', username='na66421',
                                       name='윤준기', password='qwer1234')
            category = Category.objects.create(name='프로그래밍', user=user)
            post = Post.objects.create(title='프로그래밍', content='프로그래밍', category=category,
                                       user=user)

        self.assertEqual(post.title, '프로그래밍', '포스트 제목 불일치')
        self.assertEqual(post.content, '프로그래밍', '포스트 내용 불일치')
        self.assertEqual(post.user, user, '포스트 생성 사용자 불일치')
        self.assertEqual(post.created_at, mock_date, '생성시간 불일치')
        self.assertEqual(post.modified_at, mock_date, '수정시간 불일치')
        self.assertEqual(str(post), f'{user.name}:{category.name}:{post.title}', '__str__ 불일치')
