import json

from django.contrib.auth import get_user_model

from .base_client import connectAPITest


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
        self.user2 = get_user_model().objects.create_user(
            username='na664212', name='윤준기2',
            password='qwer!@#$', is_staff=True
        )
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



