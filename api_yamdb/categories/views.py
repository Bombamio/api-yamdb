from rest_framework import viewsets, filters, generics

from api.permissions import IsAdminOrReadOnly
from .models import Category, Genre, Title
from .serializers import CategorySerializer, GenreSerializer, TitleSerializer


class CategoryAPIView(
    generics.ListCreateAPIView,
    generics.DestroyAPIView
):
    '''APIView для категорий'''
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class GenreViewSet(
        generics.ListCreateAPIView,
        generics.DestroyAPIView
    ):
    '''APIView для жанров'''
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class TitleViewSet(viewsets.ModelViewSet):
    '''ViewSet для произведений'''
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name', 'genre__slug', 'category__slug', 'year')
