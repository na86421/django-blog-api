import json

from django.contrib.auth import get_user_model

from .base_client import connectAPITest
from categories.models import Category


class CategoryViewSetTest(connectAPITest):
    def setUp(self):
        super().setUp()
        self.data = {'name': 'python', 'user': self.user.id}

    def test_create_category(self):
        res = self.client.post('/api/v1/categories/', json.dumps(self.data), content_type="application/json")
        self.assertEqual(res.status_code, 201)

    def test_create_category_already_exists(self):
        Category.objects.create(name='python', user=self.user)

        res = self.client.post('/api/v1/categories/', json.dumps(self.data), content_type="application/json")
        self.assertEqual(res.status_code, 400)

    def test_update_category_has_not_permission(self):
        test_user = get_user_model().objects.create_user(username='testuser', name='testuser', password='qwer!@#$')
        category = Category.objects.create(name='python2', user=test_user)

        update_data = {
            'name': 'Newpython2'
        }

        res = self.client.patch(f'/api/v1/categories/{category.id}/', json.dumps(update_data),
                                content_type="application/json")
        self.assertEqual(res.status_code, 403)
