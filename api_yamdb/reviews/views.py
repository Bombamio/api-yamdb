from rest_framework import viewsets
from django.shortcuts import get_object_or_404

from api.permissions import IsAuthorOrModeratorOrAdminOrReadOnly
from rest_framework.exceptions import ValidationError
from .models import Review, Comment
from categories.models import Title
from .serializers import ReviewSerializer, CommentSerializer


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

    def perform_create(self, serializer):
        title = self.get_title()

        # Проверяем, существует ли уже отзыв
        if Review.objects.filter(
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

    def get_queryset(self):
        '''Получаем комментарии для конкретного отзыва'''
        return Comment.objects.filter(review=self.get_review())

    def perform_create(self, serializer):
        '''Создание комментария с автором'''
        serializer.save(
            author=self.request.user,
            review=self.get_review()
        )
