import json

from django.contrib.auth import get_user_model

from .base_client import connectAPITest
from categories.models import Category
from posts.models import Post


class PostViewSetTest(connectAPITest):
    def setUp(self):
        super().setUp()
        self.category = Category.objects.create(name='python', user=self.user)
        self.post = Post.objects.create(title='title', content='content', category=self.category,
                                        user=self.user, is_notice='False')

    def test_retrieve_post(self):
        prev_hits = self.post.hits

        res = self.client.get(f'/api/v1/posts/{self.post.id}/')
        self.assertEqual(res.status_code, 200)
        self.assertEqual(prev_hits + 1, res.json()['hits'])

    def test_update_category_has_not_permission(self):
        test_user = get_user_model().objects.create_user(username='testuser', name='testuser', password='qwer!@#$')
        category = Category.objects.create(name='python2', user=test_user)
        post = Post.objects.create(title='title', content='content', category=category, user=test_user,
                                   is_notice='False')

        update_data = {
            'title': 'Newtitle'
        }

        res = self.client.patch(f'/api/v1/posts/{post.id}/', json.dumps(update_data), content_type="application/json")
        self.assertEqual(res.status_code, 403)

    def test_toggle_notice(self):
        data = {
            'is_notice': True
        }
        res = self.client.post(f'/api/v1/posts/{self.post.id}/toggle_notice/', json.dumps(data),
                               content_type="application/json")

        self.assertEqual(res.status_code, 200)
        self.assertTrue(Post.objects.get(id=self.post.id).is_notice)
