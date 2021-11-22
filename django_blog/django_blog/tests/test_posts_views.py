import json

from django.contrib.auth import get_user_model

from .base_client import connectAPITest
from categories.models import Category
from posts.models import Post


class PostViewSetTest(connectAPITest):
    def setUp(self):
        super().setUp()
        self.user2 = get_user_model().objects.create_user(username='na664212', name='윤준기2', password='qwer!@#$')
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
