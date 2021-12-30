from django.db.models import Q

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Post
from .serializers import PostSerializer


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def get_queryset(self):
        """
        Filter by post title, content, tags when searching with query_params.
        """
        queryset = super().get_queryset()

        if 'search' in self.request.query_params:
            search = self.request.query_params['search']

            # If you’re filtering on multiple tags, it’s very common to get duplicate results,
            # because of the way relational databases work.
            queryset = queryset.filter(
                Q(title__icontains=search) | Q(content__icontains=search) | Q(tags__name__icontains=search)
            ).distinct()

        if 'ordering' in self.request.query_params:
            # In front, Desc: '?ordering=-field_name'
            #           Asc: '?ordering=-field_name'
            ordering = self.request.query_params['ordering']

            queryset = queryset.order_by(ordering)

        return queryset

    def retrieve(self, request, *args, **kwargs):
        post = self.get_object()
        post.increase_hits()
        serializer = self.get_serializer(post)

        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def toggle_notice(self, request, pk=None):
        post = self.get_object()
        serializer = self.get_serializer(post, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)
