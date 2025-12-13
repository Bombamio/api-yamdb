# categories/views.py - ПРАВИЛЬНЫЙ ПОРЯДОК

import django_filters
from rest_framework import viewsets, status, filters, permissions
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.shortcuts import get_object_or_404

from .models import Category, Genre, Title
from .serializers import (
    CategorySerializer, GenreSerializer,
    TitleReadSerializer, TitleWriteSerializer
)
from api.permissions import IsAdminOrReadOnly


# 1. Сначала определите TitleFilter
class TitleFilter(django_filters.FilterSet):
    genre = django_filters.CharFilter(field_name='genre__slug')
    category = django_filters.CharFilter(field_name='category__slug')
    name = django_filters.CharFilter(
        field_name='name', lookup_expr='icontains')
    year = django_filters.NumberFilter(field_name='year')

    class Meta:
        model = Title
        fields = ['genre', 'category', 'name', 'year']


# 2. Потом TitleViewSet (теперь он знает о TitleFilter)
class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    filterset_class = TitleFilter  # ← Теперь работает!
    search_fields = ('name', 'description')
    http_method_names = ['get', 'post', 'patch', 'delete', 'head', 'options']

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return TitleReadSerializer
        return TitleWriteSerializer


# 3. Потом остальные ViewSets
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnly,)
    lookup_field = 'slug'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    http_method_names = ['get', 'post',
                         'delete', 'head', 'options']  # Без patch

    def retrieve(self, request, *args, **kwargs):
        # Запрещаем GET запросы к конкретной категории по slug
        if request.method == 'GET':
            return Response(
                {'detail': 'Method "GET" not allowed.'},
                status=status.HTTP_405_METHOD_NOT_ALLOWED
            )
        return super().retrieve(request, *args, **kwargs)


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrReadOnly,)
    lookup_field = 'slug'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    http_method_names = ['get', 'post',
                         'delete', 'head', 'options']  # Без patch

    def retrieve(self, request, *args, **kwargs):
        # Запрещаем GET запросы к конкретному жанру по slug
        if request.method == 'GET':
            return Response(
                {'detail': 'Method "GET" not allowed.'},
                status=status.HTTP_405_METHOD_NOT_ALLOWED
            )
        return super().retrieve(request, *args, **kwargs)
