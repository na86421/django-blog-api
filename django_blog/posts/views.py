
from rest_framework import viewsets, status
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

    def create(self, request, *args, **kwargs):
        data = request.data
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)

        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def destroy(self, request, pk=None):
        post = self.get_object()

        if not post.has_permission(request.user):
            return Response({'msg': '포스트를 생성한 유저가 아닙니다.'}, status=status.HTTP_400_BAD_REQUEST)

        post.delete()
        return Response({'msg': '포스트가 삭제되었습니다.'})

    def update(self, request, *args, **kwargs):
        post = self.get_object()
        data = request.data
        serializer = self.get_serializer(post, data=data, partial=True)
        serializer.is_valid(raise_exception=True)

        if not post.has_permission(request.user):
            return Response({'msg': '포스트를 생성한 유저가 아닙니다.'}, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response(serializer.data)
