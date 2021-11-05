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

        res = self.client.post('/signup/', json.dumps(data), content_type="application/json")
        self.assertEqual(res.status_code, 400)
        self.assertEqual(res.json()['msg'], '필수 입력항목을 입력해주세요.', 'KeyError 예외처리 실패')

        # 비밀번호 validation 실패하는 경우
        data = {
            'username': 'test',
            'name': '테스트',
            'password1': '',
            'password2': ''
        }

        res = self.client.post('/signup/', json.dumps(data), content_type="application/json")
        self.assertEqual(res.status_code, 400)
        self.assertEqual(res.json()['msg'], '비밀번호를 수정해주세요.')

        # 비밀번호가 일치하지 않는 경우
        data['password1'] = 'qwer!@#$'

        res = self.client.post('/signup/', json.dumps(data), content_type="application/json")
        self.assertEqual(res.status_code, 400)
        self.assertEqual(res.json()['msg'], '비밀번호가 일치하지 않습니다.')

        # 올바른 경우
        data['password2'] = 'qwer!@#$'

        res = self.client.post('/signup/', json.dumps(data), content_type="application/json")
        self.assertEqual(res.status_code, 201)
        self.assertEqual(res.json()['msg'], '유저가 생성되었습니다.')

        # 같은 username이 존재하는 경우
        res = self.client.post('/signup/', json.dumps(data), content_type="application/json")
        self.assertEqual(res.status_code, 400)
        self.assertEqual(res.json()['msg'], '이미 존재하는 username 입니다.')


class LoginViewTest(connectAPITest):
    def test_login(self):
        # json KeyError 발생 경우
        data = {}

        res = self.client.post('/login/', json.dumps(data), content_type="application/json")
        self.assertEqual(res.status_code, 400)
        self.assertEqual(res.json()['msg'], '필수 입력항목을 입력해주세요.', 'KeyError 예외처리 실패')

        # 로그인에 실패하는 경우
        data = {
            'username': self.user.username,
            'password': ''
        }

        res = self.client.post('/login/', json.dumps(data), content_type="application/json")
        self.assertEqual(res.status_code, 401)
        self.assertEqual(res.json()['msg'], '로그인에 실패하였습니다.')

        # 로그인에 성공하는 경우
        data['password'] = 'qwer!@#$'

        res = self.client.post('/login/', json.dumps(data), content_type="application/json")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json()['msg'], '로그인 되었습니다.')


class CategoryViewSetTest(connectAPITest):
    def test_create(self):
        # json KeyError 발생 경우
        data = {}

        res = self.client.post('/api/categorys/', json.dumps(data), content_type="application/json")
        self.assertEqual(res.status_code, 400)
        self.assertEqual(res.json()['msg'], '필수 입력항목을 입력해주세요.', 'KeyError 예외처리 실패')

        # 올바른 경우
        data['name'] = 'python'
        res = self.client.post('/api/categorys/', json.dumps(data), content_type="application/json")
        self.assertEqual(res.status_code, 201)
        self.assertEqual(res.json()['msg'], '카테고리가 생성되었습니다.', '카테고리 생성 실패')
        self.assertEqual(res.json()['category']['user'], self.user.id, '카테고리 생성 유저 불일치')

        # 동일한 카테고리명일 경우
        res = self.client.post('/api/categorys/', json.dumps(data), content_type="application/json")
        self.assertEqual(res.status_code, 400)
        self.assertEqual(res.json()['msg'], '이미 존재하는 카테고리명 입니다.',
                         '동일한 이름을 가진 카테고리 생성 금지 실패')

    def test_destroy(self):
        user2 = User.objects.create_user(username='na664212', name='윤준기2', password='qwer!@#$')
        category = Category.objects.create(name='python', user=self.user)
        category2 = Category.objects.create(name='python', user=user2)

        # 올바른 경우
        res = self.client.delete(f'/api/categorys/{category.id}/')
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json()['msg'], '카테고리가 삭제되었습니다.', '카테고리 삭제 실패')

        # 카테고리를 생성한 유저가 아닐 경우
        res = self.client.delete(f'/api/categorys/{category2.id}/')
        self.assertEqual(res.status_code, 400)
        self.assertEqual(res.json()['msg'], '카테고리를 생성한 유저가 아닙니다.')

    def test_update(self):
        user2 = User.objects.create_user(username='na664212', name='윤준기2', password='qwer!@#$')
        category = Category.objects.create(name='python', user=self.user)
        category2 = Category.objects.create(name='python', user=user2)

        # json KeyError 발생 경우
        data = {}
        res = self.client.patch(f'/api/categorys/{category.id}/', json.dumps(data),
                                content_type="application/json")
        self.assertEqual(res.status_code, 400)
        self.assertEqual(res.json()['msg'], '필수 입력항목을 입력해주세요.', 'KeyError 예외처리 실패')

        # 올바른 경우
        data['name'] = 'django'
        res = self.client.patch(f'/api/categorys/{category.id}/', json.dumps(data),
                                content_type="application/json")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json()['msg'], '카테고리 이름이 변경되었습니다.', '카테고리 수정 실패')
        self.assertEqual(res.json()['category']['name'], data['name'], '카테고리 수정 실패')

        # 카테고리를 생성한 유저가 아닐 경우
        res = self.client.patch(f'/api/categorys/{category2.id}/', json.dumps(data),
                                content_type="application/json")
        self.assertEqual(res.status_code, 400)
        self.assertEqual(res.json()['msg'], '카테고리를 생성한 유저가 아닙니다.')
        
