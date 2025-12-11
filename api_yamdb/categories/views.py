from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, filters

from api.permissions import IsAdminOrReadOnly
from .models import Category, Genre, Title
from .serializers import CategorySerializer, GenreSerializer, TitleSerializer


# Category fields.

class CategoryViewSet(viewsets.ModelViewSet):
    '''ViewSet для категорий'''
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'slug'
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


# Genre fields.

class GenreViewSet(viewsets.ModelViewSet):
    '''ViewSet для жанров'''
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    lookup_field = 'slug'
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


# Title fields.

class TitleViewSet(viewsets.ModelViewSet):
    '''ViewSet для произведений'''
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = (DjangoFilterBackend,)
    filterset_fields  = ('category__slug', 'genre__slug', 'name', 'year')
