from django.test import TestCase
from django.contrib.auth import get_user_model

from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient


class connectAPITest(TestCase):
    def setUp(self):
        print(f'-------{self._testMethodName}-------')
        self.user = get_user_model().objects.create_user(username='na66421', name='윤준기', password='qwer!@#$')
        self.token = Token.objects.create(user=self.user)

        # 테스트 clinet에서는 Authentication을 무시한다.
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def tearDown(self):
        del self.client
        del self.user
