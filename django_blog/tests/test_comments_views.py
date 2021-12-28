import json

from django.contrib.auth import get_user_model

from .base_client import connectAPITest
from categories.models import Category
from posts.models import Post
from comments.models import Comment


class CommentViewSetTest(connectAPITest):
    def setUp(self):
        super().setUp()
        self.category = Category.objects.create(name='python', user=self.user)
        self.post = Post.objects.create(
            title='title', content='content', category=self.category, user=self.user, is_notice='False'
        )
        self.comment = Comment.objects.create(content='comment', post=self.post, user=self.user)

    def test_update_comment(self):
        update_data = {
            'content': 'NewComment'
        }

        res = self.client.patch(
            f'/api/v1/comments/{self.comment.id}/', json.dumps(update_data), content_type="application/json"
        )
        self.assertEqual(res.status_code, 200)

    def test_update_comment_changed_user(self):
        test_user = get_user_model().objects.create_user(username='testuser', name='testuser', password='qwer!@#$')
        update_data = {
            'user': test_user.id
        }

        res = self.client.patch(
            f'/api/v1/comments/{self.comment.id}/', json.dumps(update_data), content_type="application/json"
        )
        self.assertEqual(res.status_code, 400)
