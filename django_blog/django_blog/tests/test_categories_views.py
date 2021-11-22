import json

from django.contrib.auth import get_user_model

from .base_client import connectAPITest
from categories.models import Category


class CategoryViewSetTest(connectAPITest):
    def setUp(self):
        super().setUp()
        self.user2 = get_user_model().objects.create_user(username='na664212', name='윤준기2', password='qwer!@#$')
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
