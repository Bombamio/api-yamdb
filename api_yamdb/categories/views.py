# categories/views.py - ПРАВИЛЬНЫЙ ПОРЯДОК

import django_filters
from rest_framework import viewsets, status, filters
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from .models import Category, Genre, Title
from .serializers import (
    CategorySerializer, GenreSerializer,
    TitleReadSerializer, TitleWriteSerializer
)
from api.permissions import IsAdminOrReadOnly


class SlugBaseViewSet(viewsets.ModelViewSet):
    '''Базовый ViewSet для моделей со slug.'''
    permission_classes = (IsAdminOrReadOnly,)
    lookup_field = 'slug'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    http_method_names = ['get', 'post', 'delete', 'head', 'options']

    def retrieve(self, request, *args, **kwargs):
        # Запрещаем GET запросы к конкретному объекту по slug
        if request.method == 'GET':
            return Response(
                {'detail': 'Method "GET" not allowed.'},
                status=status.HTTP_405_METHOD_NOT_ALLOWED
            )
        return super().retrieve(request, *args, **kwargs)


class TitleFilter(django_filters.FilterSet):
    genre = django_filters.CharFilter(field_name='genre__slug')
    category = django_filters.CharFilter(field_name='category__slug')
    name = django_filters.CharFilter(
        field_name='name', lookup_expr='icontains')
    year = django_filters.NumberFilter(field_name='year')

    class Meta:
        model = Title
        fields = ['genre', 'category', 'name', 'year']


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    filterset_class = TitleFilter
    search_fields = ('name', 'description')
    http_method_names = ['get', 'post', 'patch', 'delete', 'head', 'options']

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return TitleReadSerializer
        return TitleWriteSerializer


class CategoryViewSet(SlugBaseViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(SlugBaseViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
