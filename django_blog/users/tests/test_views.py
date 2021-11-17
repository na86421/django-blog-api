import json

from django.test import TestCase
from django.contrib.auth import get_user_model

from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from ..models import Category, Post


User = get_user_model()


class connectAPITest(TestCase):
    def setUp(self):
        print(f'-------{self._testMethodName}-------')
        self.user = User.objects.create_user(username='na66421', name='윤준기', password='qwer!@#$')
        self.token = Token.objects.create(user=self.user)

        # 테스트 clinet에서는 Authentication을 무시한다.
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def tearDown(self):
        del self.client
        del self.user


class SignUpViewTest(connectAPITest):
    def setUp(self):
        super().setUp()
        self.data = {
            'username': 'test',
            'name': '테스트',
            'password1': 'qwer!@#$',
            'password2': 'qwer!@#$',
        }

    def test_signup(self):
        res = self.client.post('/accounts/signup/', json.dumps(self.data), content_type="application/json")
        self.assertEqual(res.status_code, 201)

    def test_signup_invalid_data(self):
        self.data = {}

        res = self.client.post('/accounts/signup/', json.dumps(self.data), content_type="application/json")
        self.assertEqual(res.status_code, 400)

    def test_signup_invalid_password(self):
        self.data['password1'] = ''
        self.data['password2'] = ''

        res = self.client.post('/accounts/signup/', json.dumps(self.data), content_type="application/json")
        self.assertEqual(res.status_code, 400)

    def test_signup_not_eqaul_password(self):
        self.data['password1'] = 'qwer1234'

        res = self.client.post('/accounts/signup/', json.dumps(self.data), content_type="application/json")
        self.assertEqual(res.status_code, 400)

    def test_signup_already_exists(self):
        self.data['username'] = 'na66421'

        res = self.client.post('/accounts/signup/', json.dumps(self.data), content_type="application/json")
        self.assertEqual(res.status_code, 400)


class SignInViewTest(connectAPITest):
    def setUp(self):
        super().setUp()
        self.data = {
            'username': self.user.username,
            'password': 'qwer!@#$',
        }

    def test_signin(self):
        res = self.client.post('/accounts/signin/', json.dumps(self.data), content_type="application/json")
        self.assertEqual(res.status_code, 200)

    def test_signin_invalid_data(self):
        self.data = {}

        res = self.client.post('/accounts/signin/', json.dumps(self.data), content_type="application/json")
        self.assertEqual(res.status_code, 400)

    def test_signin_invalid_password(self):
        self.data['password'] = 'qwer1234'

        res = self.client.post('/accounts/signin/', json.dumps(self.data), content_type="application/json")
        self.assertEqual(res.status_code, 401)


class UserViewSetTest(connectAPITest):
    def setUp(self):
        super().setUp()
        self.user2 = User.objects.create_user(username='na664212', name='윤준기2', password='qwer!@#$',
                                              is_staff=True)
        self.data = {
            'name': 'name',
            'password': 'qwer!@#$'
        }

    def test_update_user(self):
        res = self.client.patch(f'/api/v1/users/{self.user.id}/', json.dumps(self.data),
                                content_type="application/json")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json()['name'], self.data['name'], '프로필 수정 실패')

    def test_update_invalid_data(self):
        self.data = {}

        res = self.client.patch(f'/api/v1/users/{self.user.id}/', json.dumps(self.data),
                                content_type="application/json")
        self.assertEqual(res.status_code, 400)

    def test_update_invalid_password(self):
        self.data['password'] = ''

        res = self.client.patch(f'/api/v1/users/{self.user.id}/', json.dumps(self.data),
                                content_type="application/json")
        self.assertEqual(res.status_code, 400)

    def test_update_not_me(self):
        res = self.client.patch(f'/api/v1/users/{self.user2.id}/', json.dumps(self.data),
                                content_type="application/json")
        self.assertEqual(res.status_code, 400)


class CategoryViewSetTest(connectAPITest):
    def setUp(self):
        super().setUp()
        self.user2 = User.objects.create_user(username='na664212', name='윤준기2', password='qwer!@#$')
        self.category = Category.objects.create(name='python', user=self.user)
        self.category2 = Category.objects.create(name='python', user=self.user2)

        self.data = {'name': 'python', 'user': self.user.id}

    def test_create_category(self):
        self.data['name'] = 'python2'

        res = self.client.post('/api/v1/categories/', json.dumps(self.data),
                               content_type="application/json")
        self.assertEqual(res.status_code, 201)

    def test_create_category_invalid_data(self):
        self.data = {}

        res = self.client.post('/api/v1/categories/', json.dumps(self.data),
                               content_type="application/json")
        self.assertEqual(res.status_code, 400)

    def test_create_category_already_exists(self):
        res = self.client.post('/api/v1/categories/', json.dumps(self.data),
                               content_type="application/json")
        self.assertEqual(res.status_code, 400)

    def test_destroy_category(self):
        res = self.client.delete(f'/api/v1/categories/{self.category.id}/')
        self.assertEqual(res.status_code, 200)
        self.assertFalse(Category.objects.filter(id=self.category.id).exists())

    def test_destory_category_not_created_user(self):
        res = self.client.delete(f'/api/v1/categories/{self.category2.id}/')
        self.assertEqual(res.status_code, 400)

    def test_update_category(self):
        self.data['name'] = 'django'

        res = self.client.patch(f'/api/v1/categories/{self.category.id}/', json.dumps(self.data),
                                content_type="application/json")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json()['name'], self.data['name'], '카테고리 수정 실패')

    def test_update_category_invalid_data(self):
        self.data = {}

        res = self.client.patch(f'/api/v1/categories/{self.category.id}/', json.dumps(self.data),
                                content_type="application/json")
        self.assertEqual(res.status_code, 400)

    def test_update_category_not_created_user(self):
        res = self.client.patch(f'/api/v1/categories/{self.category2.id}/', json.dumps(self.data),
                                content_type="application/json")
        self.assertEqual(res.status_code, 400)

    def test_update_category_already_exists(self):
        res = self.client.patch(f'/api/v1/categories/{self.category.id}/', json.dumps(self.data),
                                content_type="application/json")
        self.assertEqual(res.status_code, 400)


class PostViewSetTest(connectAPITest):
    def setUp(self):
        super().setUp()
        self.user2 = User.objects.create_user(username='na664212', name='윤준기2', password='qwer!@#$')
        self.category = Category.objects.create(name='python', user=self.user)
        self.category2 = Category.objects.create(name='python2', user=self.user2)
        self.post = Post.objects.create(title='title', content='content', category=self.category,
                                        user=self.user)
        self.post2 = Post.objects.create(title='title', content='content', category=self.category,
                                         user=self.user2)

        self.data = {
            'title': 'title',
            'content': 'content',
            'category': self.category.id,
            'user': self.user.id,
        }

    def test_retrieve_post(self):
        res = self.client.get(f'/api/v1/posts/{self.post.id}/')
        self.assertEqual(res.status_code, 200)

    def test_create_post(self):
        res = self.client.post('/api/v1/posts/', json.dumps(self.data),
                               content_type="application/json")
        self.assertEqual(res.status_code, 201)

    def test_create_post_invalid_data(self):
        self.data = {}

        res = self.client.post('/api/v1/posts/', json.dumps(self.data),
                               content_type="application/json")
        self.assertEqual(res.status_code, 400)

    def test_destroy_post(self):
        res = self.client.delete(f'/api/v1/posts/{self.post.id}/', content_type="application/json")
        self.assertEqual(res.status_code, 200)
        self.assertFalse(Post.objects.filter(id=self.post.id).exists())

    def test_destroy_post_not_created_user(self):
        res = self.client.delete(f'/api/v1/posts/{self.post2.id}/', content_type="application/json")
        self.assertEqual(res.status_code, 400)

    def test_update_post(self):
        self.data['title'] = 'update_title'
        self.data['content'] = 'update_content'
        self.data['category'] = self.category2.id

        res = self.client.patch(f'/api/v1/posts/{self.post.id}/', json.dumps(self.data),
                                content_type="application/json")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json()['title'], self.data['title'], '포스트 수정 실패')
        self.assertEqual(res.json()['content'], self.data['content'], '포스트 수정 실패')
        self.assertEqual(res.json()['category'], self.data['category'], '포스트 수정 실패')

    def test_update_post_invalid_data(self):
        self.data = {}

        res = self.client.patch(f'/api/v1/posts/{self.post.id}/', json.dumps(self.data),
                                content_type="application/json")
        self.assertEqual(res.status_code, 400)

    def test_update_post_not_created_user(self):
        res = self.client.patch(f'/api/v1/posts/{self.post2.id}/', json.dumps(self.data),
                                content_type="application/json")
        self.assertEqual(res.status_code, 400)
