from unittest import mock

from django.contrib.auth import get_user_model
from django.utils import timezone
from django.test import TestCase

class UserModelTest(TestCase):
    def setUp(self):
        self.user = get_user_model()
        
    def tearDown(self):
        del self.user

    def test_default_values(self):
        mock_date = timezone.now()
        with mock.patch('django.utils.timezone.now') as mock_now:
            mock_now.return_value = mock_date
            user = self.user.objects.create(email='na66421@gmail.com', username='na66421',
                                            name='윤준기', password='qwer1234')

        self.assertEqual(user.email, 'na66421@gmail.com', "email 불일치")
        self.assertEqual(user.username, 'na66421', "username 불일치")
        self.assertEqual(user.name, '윤준기', "name 불일치")
        self.assertEqual(user.password, 'qwer1234', "password 불일치")
        self.assertEqual(user.created_at, mock_date, "생성시간 불일치")
        self.assertEqual(user.modified_at, mock_date, "수정시간 불일치")
        self.assertEqual(str(user), user.name, "__str__ 불일치")
