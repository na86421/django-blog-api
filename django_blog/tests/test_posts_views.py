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

    def test_search_post(self):
        param = f'?search={self.post.title}'

        res = self.client.get('/api/v1/posts/' + param)
        self.assertEqual(res.json()['count'], Post.objects.filter(title=self.post.title).count())

    def test_retrieve_post(self):
        prev_hits = self.post.hits

        res = self.client.get(f'/api/v1/posts/{self.post.id}/')
        self.assertEqual(res.status_code, 200)
        self.assertEqual(prev_hits + 1, res.json()['hits'])

    def test_update_post(self):
        update_data = {
            'title': 'Newtitle'
        }

        res = self.client.patch(
            f'/api/v1/posts/{self.post.id}/', json.dumps(update_data), content_type="application/json"
        )
        self.assertEqual(res.status_code, 200)

    def test_update_post_changed_user(self):
        test_user = get_user_model().objects.create_user(username='testuser', name='testuser', password='qwer!@#$')
        update_data = {
            'user': test_user.id
        }

        res = self.client.patch(
            f'/api/v1/posts/{self.post.id}/', json.dumps(update_data), content_type="application/json"
        )
        self.assertEqual(res.status_code, 400)

    def test_post_toggle_notice(self):
        data = {
            'is_notice': True
        }
        res = self.client.post(f'/api/v1/posts/{self.post.id}/toggle_notice/', json.dumps(data),
                               content_type="application/json")

        self.assertEqual(res.status_code, 200)
        self.assertTrue(Post.objects.get(id=self.post.id).is_notice)
