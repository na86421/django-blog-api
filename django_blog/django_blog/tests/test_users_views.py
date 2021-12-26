import json

from django.contrib.auth import get_user_model

from .base_client import connectAPITest


class SignUpViewTest(connectAPITest):
    def setUp(self):
        super().setUp()
        self.signup_data = {
            'username': 'test',
            'name': '테스트',
            'password': 'qwer!@#$'
        }

    def test_signup(self):
        res = self.client.post('/api/v1/users/signup/', json.dumps(self.signup_data), content_type="application/json")
        self.assertEqual(res.status_code, 201)

    def test_signup_with_simple_pasword(self):
        self.signup_data['password'] = 'qwer1234'

        res = self.client.post('/api/v1/users/signup/', json.dumps(self.signup_data), content_type="application/json")
        self.assertEqual(res.status_code, 400)

    def test_signup_password_encryption(self):
        res = self.client.post('/api/v1/users/signup/', json.dumps(self.signup_data), content_type="application/json")
        created_user = get_user_model().objects.get(id=res.json()['id'])

        self.assertEqual(res.status_code, 201)
        self.assertNotEqual(created_user.password, self.signup_data['password'])


class SignInViewTest(connectAPITest):
    def setUp(self):
        super().setUp()
        self.signin_data = {
            'username': self.user.username,
            'password': 'qwer!@#$',
        }

    def test_signin(self):
        res = self.client.post('/api/v1/users/signin/', json.dumps(self.signin_data), content_type="application/json")
        self.assertEqual(res.status_code, 200)

    def test_signin_invalid_password(self):
        self.signin_data['password'] = '3434'
        res = self.client.post('/api/v1/users/signin/', json.dumps(self.signin_data), content_type="application/json")
        self.assertEqual(res.status_code, 401)


class UserViewSetTest(connectAPITest):
    def test_update_user_has_not_permission(self):
        test_user = get_user_model().objects.create_user(username='testuser', name='testuser', password='qwer!@#$')
        update_data = {
            'name': 'Newtestuser'
        }

        res = self.client.patch(f'/api/v1/users/{test_user.id}/', json.dumps(update_data),
                                content_type="application/json")
        self.assertEqual(res.status_code, 403)
