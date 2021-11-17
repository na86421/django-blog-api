from rest_framework import viewsets, status
from rest_framework.response import Response

from .models import Category
from .serializers import CategorySerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def create(self, request, *args, **kwargs):
        data = request.data
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)

        if Category.objects.filter(name=data['name']).exists():
            return Response({'msg': '이미 존재하는 카테고리명 입니다.'}, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def destroy(self, request, pk=None):
        category = self.get_object()

        if not category.has_permission(request.user):
            return Response({'msg': '카테고리를 생성한 유저가 아닙니다.'}, status=status.HTTP_400_BAD_REQUEST)

        category.delete()
        return Response({'msg': '카테고리가 삭제되었습니다.'})

    def update(self, request, *args, **kwargs):
        category = self.get_object()
        data = request.data
        serializer = self.get_serializer(category, data=data, partial=True)
        serializer.is_valid(raise_exception=True)

        if not category.has_permission(request.user):
            return Response({'msg': '카테고리를 생성한 유저가 아닙니다.'}, status=status.HTTP_400_BAD_REQUEST)

        if Category.objects.filter(name=data['name']).exclude(id=category.id).exists():
            return Response({'msg': '이미 존재하는 카테고리명 입니다.'}, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response(serializer.data)
