from rest_framework import viewsets, filters, generics

from api.permissions import IsAdmin, IsAdminOrReadOnly
from .models import Category, Genre, Title
from .serializers import CategorySerializer, GenreSerializer, TitleSerializer


# Category fields.

class CategoryListCreateView(generics.ListCreateAPIView):
    '''ListView для категорий'''
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class CategoryDestroyView(generics.DestroyAPIView):
    '''APIView для категорий'''
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdmin]


# Genre fields.

class GenreListCreateView(generics.ListCreateAPIView):
    '''ListView для жанров'''
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class GenreDestroyView(generics.DestroyAPIView):
    '''APIView для жанров'''
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [IsAdmin]


# Title fields.

class TitleViewSet(viewsets.ModelViewSet):
    '''ViewSet для произведений'''
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name', 'genre__slug', 'category__slug', 'year')
