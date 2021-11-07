import json

from django.test import TestCase
from django.contrib.auth import get_user_model

from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from blog.models import Category, Post
from blog.api.serializers import UserSerializer, CategorySerializer, PostSerializer


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
    def test_create_user(self):
        # json KeyError 발생 경우
        data = {}

        res = self.client.post('/accounts/signup/', json.dumps(data), content_type="application/json")
        self.assertEqual(res.status_code, 400)
        self.assertEqual(res.json()['msg'], '필수 입력항목을 입력해주세요.', 'KeyError 예외처리 실패')

        # 비밀번호 validation 실패하는 경우
        data = {
            'username': 'test',
            'name': '테스트',
            'password1': '',
            'password2': ''
        }

        res = self.client.post('/accounts/signup/', json.dumps(data), content_type="application/json")
        self.assertEqual(res.status_code, 400)
        self.assertEqual(res.json()['msg'], '비밀번호를 수정해주세요.')

        # 비밀번호가 일치하지 않는 경우
        data['password1'] = 'qwer!@#$'

        res = self.client.post('/accounts/signup/', json.dumps(data), content_type="application/json")
        self.assertEqual(res.status_code, 400)
        self.assertEqual(res.json()['msg'], '비밀번호가 일치하지 않습니다.')

        # 올바른 경우
        data['password2'] = 'qwer!@#$'

        res = self.client.post('/accounts/signup/', json.dumps(data), content_type="application/json")
        self.assertEqual(res.status_code, 201)
        self.assertEqual(res.json()['msg'], '유저가 생성되었습니다.')

        # 같은 username이 존재하는 경우
        res = self.client.post('/accounts/signup/', json.dumps(data), content_type="application/json")
        self.assertEqual(res.status_code, 400)
        self.assertEqual(res.json()['msg'], '이미 존재하는 username 입니다.')


class SignInViewTest(connectAPITest):
    def test_login(self):
        # json KeyError 발생 경우
        data = {}

        res = self.client.post('/accounts/signin/', json.dumps(data), content_type="application/json")
        self.assertEqual(res.status_code, 400)
        self.assertEqual(res.json()['msg'], '필수 입력항목을 입력해주세요.', 'KeyError 예외처리 실패')

        # 로그인에 실패하는 경우
        data = {
            'username': self.user.username,
            'password': ''
        }

        res = self.client.post('/accounts/signin/', json.dumps(data), content_type="application/json")
        self.assertEqual(res.status_code, 401)
        self.assertEqual(res.json()['msg'], '로그인에 실패하였습니다.')

        # 로그인에 성공하는 경우
        data['password'] = 'qwer!@#$'

        res = self.client.post('/accounts/signin/', json.dumps(data), content_type="application/json")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json()['msg'], '로그인 되었습니다.')


class CategoryViewSetTest(connectAPITest):
    def test_create(self):
        # json KeyError 발생 경우
        data = {}

        res = self.client.post('/api/v1/categories/', json.dumps(data), content_type="application/json")
        self.assertEqual(res.status_code, 400)
        self.assertEqual(res.json()['msg'], '필수 입력항목을 입력해주세요.', 'KeyError 예외처리 실패')

        # 올바른 경우
        data['name'] = 'python'
        res = self.client.post('/api/v1/categories/', json.dumps(data), content_type="application/json")
        self.assertEqual(res.status_code, 201)
        self.assertEqual(res.json()['msg'], '카테고리가 생성되었습니다.', '카테고리 생성 실패')
        self.assertEqual(res.json()['category']['user'], self.user.id, '카테고리 생성 유저 불일치')

        # 동일한 카테고리명일 경우
        res = self.client.post('/api/v1/categories/', json.dumps(data), content_type="application/json")
        self.assertEqual(res.status_code, 400)
        self.assertEqual(res.json()['msg'], '이미 존재하는 카테고리명 입니다.',
                         '동일한 이름을 가진 카테고리 생성 금지 실패')

    def test_destroy(self):
        user2 = User.objects.create_user(username='na664212', name='윤준기2', password='qwer!@#$')
        category = Category.objects.create(name='python', user=self.user)
        category2 = Category.objects.create(name='python', user=user2)

        # 올바른 경우
        res = self.client.delete(f'/api/v1/categories/{category.id}/')
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json()['msg'], '카테고리가 삭제되었습니다.', '카테고리 삭제 실패')

        # 카테고리를 생성한 유저가 아닐 경우
        res = self.client.delete(f'/api/v1/categories/{category2.id}/')
        self.assertEqual(res.status_code, 400)
        self.assertEqual(res.json()['msg'], '카테고리를 생성한 유저가 아닙니다.')

    def test_update(self):
        user2 = User.objects.create_user(username='na664212', name='윤준기2', password='qwer!@#$')
        category = Category.objects.create(name='python', user=self.user)
        category2 = Category.objects.create(name='python2', user=user2)

        # json KeyError 발생 경우
        data = {}
        res = self.client.patch(f'/api/v1/categories/{category.id}/', json.dumps(data),
                                content_type="application/json")
        self.assertEqual(res.status_code, 400)
        self.assertEqual(res.json()['msg'], '필수 입력항목을 입력해주세요.', 'KeyError 예외처리 실패')

        # 올바른 경우
        data['name'] = 'django'
        res = self.client.patch(f'/api/v1/categories/{category.id}/', json.dumps(data),
                                content_type="application/json")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json()['msg'], '카테고리 이름이 변경되었습니다.', '카테고리 수정 실패')
        self.assertEqual(res.json()['category']['name'], data['name'], '카테고리 수정 실패')

        # 이미 존재하는 카테고리명인 경우
        data['name'] = 'python2'
        res = self.client.patch(f'/api/v1/categories/{category.id}/', json.dumps(data),
                                content_type="application/json")
        self.assertEqual(res.status_code, 400)
        self.assertEqual(res.json()['msg'], '이미 존재하는 카테고리명 입니다.')

        # 카테고리를 생성한 유저가 아닐 경우
        res = self.client.patch(f'/api/v1/categories/{category2.id}/', json.dumps(data),
                                content_type="application/json")
        self.assertEqual(res.status_code, 400)
        self.assertEqual(res.json()['msg'], '카테고리를 생성한 유저가 아닙니다.')
        

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


    def test_create(self):
        # json KeyError 발생 경우
        data = {}

        res = self.client.post('/api/v1/posts/', json.dumps(data), content_type="application/json")
        self.assertEqual(res.status_code, 400)
        self.assertEqual(res.json()['msg'], '필수 입력항목을 입력해주세요.', 'KeyError 예외처리 실패')

        # 올바른 경우
        category = Category.objects.create(name='python', user=self.user)
        data = {
            'title': 'title',
            'content': 'content',
            'category_id': category.id,
        }

        res = self.client.post('/api/v1/posts/', json.dumps(data), content_type="application/json")
        self.assertEqual(res.status_code, 201)
        self.assertEqual(res.json()['msg'], '포스트가 생성되었습니다.', '포스트 생성 실패')
        self.assertEqual(res.json()['post']['user'], self.user.id, '포스트 생성 유저 불일치')

    def test_destroy(self):
        # 올바른 경우
        res = self.client.delete(f'/api/v1/posts/{self.post.id}/', content_type="application/json")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json()['msg'], '포스트가 삭제되었습니다.', '포스트 삭제 실패')
        
        # 포스트를 생성한 유저가 아닌 경우
        res = self.client.delete(f'/api/v1/posts/{self.post2.id}/', content_type="application/json")
        self.assertEqual(res.status_code, 400)
        self.assertEqual(res.json()['msg'], '포스트를 생성한 유저가 아닙니다.')


    def test_update(self):
        # json KeyError 발생 경우
        data = {}
        res = self.client.patch(f'/api/v1/posts/{self.post.id}/', json.dumps(data),
                                content_type="application/json")
        self.assertEqual(res.status_code, 400)
        self.assertEqual(res.json()['msg'], '필수 입력항목을 입력해주세요.', 'KeyError 예외처리 실패')

        # 올바른 경우
        data = {
            'title': 'title_change',
            'content': 'content_change',
        }
        res = self.client.patch(f'/api/v1/posts/{self.post.id}/', json.dumps(data),
                                content_type="application/json")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json()['msg'], '포스트가 변경되었습니다.', '포스트 수정 실패')
        self.assertEqual(res.json()['post']['title'], data['title'], '포스트 수정 실패')
        self.assertEqual(res.json()['post']['content'], data['content'], '포스트 수정 실패')

        # 포스트를 생성한 유저가 아닐 경우
        res = self.client.patch(f'/api/v1/posts/{self.post2.id}/', json.dumps(data),
                                content_type="application/json")
        self.assertEqual(res.status_code, 400)
        self.assertEqual(res.json()['msg'], '포스트를 생성한 유저가 아닙니다.')

    def test_change_category(self):
        # json KeyError 발생 경우
        data = {}
        res = self.client.patch(f'/api/v1/posts/{self.post.id}/change_category/', json.dumps(data),
                                content_type="application/json")
        self.assertEqual(res.status_code, 400)
        self.assertEqual(res.json()['msg'], '필수 입력항목을 입력해주세요.', 'KeyError 예외처리 실패')

        # 포스트를 생성한 유저가 아닐 경우
        res = self.client.patch(f'/api/v1/posts/{self.post2.id}/change_category/', json.dumps(data),
                                content_type="application/json")
        self.assertEqual(res.status_code, 400)
        self.assertEqual(res.json()['msg'], '포스트를 생성한 유저가 아닙니다.')

        # 유효하지 않은 카테고리인 경우
        data['category_id'] = '9999'
        res = self.client.patch(f'/api/v1/posts/{self.post.id}/change_category/', json.dumps(data),
                                content_type="application/json")
        self.assertEqual(res.status_code, 400)
        self.assertEqual(res.json()['msg'], '유효한 카테고리가 아닙니다.')

        # 올바른 경우
        data['category_id'] = self.category2.id
        res = self.client.patch(f'/api/v1/posts/{self.post.id}/change_category/', json.dumps(data),
                                content_type="application/json")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json()['msg'], '포스트의 카테고리가 변경되었습니다.')
