
from rest_framework import viewsets
from rest_framework.response import Response

from .models import Post
from .serializers import PostSerializer


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def retrieve(self, request, *args, **kwargs):
        post = self.get_object()
        post.increase_hits()
        serializer = self.get_serializer(post)
        return Response(serializer.data)
