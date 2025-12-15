import django_filters

from django.shortcuts import get_object_or_404

from rest_framework import filters, status, viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from django_filters.rest_framework import DjangoFilterBackend

from categories.models import Category, Genre, Title
from reviews.models import Comment, Review

from .permissions import (
    IsAdminOrReadOnly,
    IsAuthorOrModeratorOrAdminOrReadOnly,
)
from .serializers import (
    CategorySerializer,
    CommentSerializer,
    GenreSerializer,
    ReviewSerializer,
    TitleReadSerializer,
    TitleWriteSerializer,
)


# Categories fields.

class SlugBaseViewSet(viewsets.ModelViewSet):
    # TODO: Чтобы не прописывать метод retrieve ниже, используем вместо
    # ModelViewSet при наследовании GenericViewSet и набор миксинов.
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
    # TODO: Фильтры убираем в отдельный файл - filters.py
    genre = django_filters.CharFilter(field_name='genre__slug')
    category = django_filters.CharFilter(field_name='category__slug')
    name = django_filters.CharFilter(
        field_name='name', lookup_expr='icontains')
        # Можно лучше: Удачная настройка lookup_expr. Такая же подойдет
        # и для двух полей выше.
    year = django_filters.NumberFilter(field_name='year')
    # TODO: Это поле прописывать не надо. FilterSet справится с ним сам,
    # достаточно добавить его в перечень fields

    class Meta:
        model = Title
        fields = ['genre', 'category', 'name', 'year']


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    # TODO: Тут надо применить аннотацию, чтобы добавить данные о
    # рейтинге для всех объектов в кверисете при их получении из БД.
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
    # Отлично: Повторяющиеся настройки вынесены в базовый класс.
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(SlugBaseViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


# Review fields.

class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthorOrModeratorOrAdminOrReadOnly]
    http_method_names = ['get', 'post', 'patch', 'delete', 'head', 'options']

    def get_title(self):
        '''Получаем произведение по ID из URL'''
        return get_object_or_404(Title, id=self.kwargs.get('title_id'))

    def get_queryset(self):
        '''Получаем отзывы для конкретного произведения'''
        return Review.objects.filter(title=self.get_title())
        # TODO: Получим отзывы через объект произведения и related_name

    def perform_create(self, serializer):
        title = self.get_title()

        # Проверяем, существует ли уже отзыв
        if Review.objects.filter(
        # TODO: Валидация убираем в сериализатор.
            title=title, author=self.request.user
        ).exists():
            raise ValidationError(
                {'detail': 'Вы уже оставили отзыв на это произведение.'}
            )

        serializer.save(
            author=self.request.user,
            title=title
        )


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthorOrModeratorOrAdminOrReadOnly]
    http_method_names = ['get', 'post', 'patch', 'delete', 'head', 'options']

    def get_review(self):
        '''Получаем отзыв по ID из URL'''
        return get_object_or_404(Review, id=self.kwargs.get('review_id'))
        # TODO: Необходимо проверить не только id ревью, полученное в
        # запросе, но и id произведения. Добавьте еще один фильтр по id
        # произведения в этот запрос.

    def get_queryset(self):
        '''Получаем комментарии для конкретного отзыва'''
        return Comment.objects.filter(review=self.get_review())
        # TODO: Получим комментарии через объект отзыва и related_name

    def perform_create(self, serializer):
        '''Создание комментария с автором'''
        serializer.save(
            author=self.request.user,
            review=self.get_review()
        )
