from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, filters

from api.permissions import IsAdminOrReadOnly
from .models import Category, Genre, Title
from . import serializers

# Category fields.

class CategoryViewSet(viewsets.ModelViewSet):
    '''ViewSet для категорий'''
    queryset = Category.objects.all()
    serializer_class = serializers.CategorySerializer
    lookup_field = 'slug'
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


# Genre fields.

class GenreViewSet(viewsets.ModelViewSet):
    '''ViewSet для жанров'''
    queryset = Genre.objects.all()
    serializer_class = serializers.GenreSerializer
    lookup_field = 'slug'
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


# Title fields.

class TitleViewSet(viewsets.ReadOnlyModelViewSet):
    '''ViewSet для произведений'''
    queryset = Title.objects.all()
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = (DjangoFilterBackend,)
    filterset_fields  = ('category__slug', 'genre__slug', 'name', 'year')

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return serializers.TitleReadSerializer
        return serializers.TitleWriteSerializer
