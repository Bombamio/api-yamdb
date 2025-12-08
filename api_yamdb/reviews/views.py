from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Review, Comment
from .serializers import ReviewSerializer, CommentSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    '''ViewSet для отзывов'''
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        '''Получаем отзывы для конкретного произведения'''
        title_id = self.kwargs.get('title_id')
        return Review.objects.filter(title_id=title_id)

    def perform_create(self, serializer):
        '''Создание отзыва с автором'''
        title_id = self.kwargs.get('title_id')

        # Сохраняем заглушку author_id (позже заменим на ForeignKey)
        serializer.save(
            title_id=title_id,
            author_id=self.request.user.id if self.request.user.is_authenticated else None
        )


class CommentViewSet(viewsets.ModelViewSet):
    '''ViewSet для комментариев к отзывам'''
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        '''Получаем комментарии для конкретного отзыва'''
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, id=review_id)
        return Comment.objects.filter(review=review)

    def perform_create(self, serializer):
        '''Создание комментария с автором'''
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, id=review_id)

        # Сохраняем заглушку author_id
        serializer.save(
            review=review,
            author_id=self.request.user.id if self.request.user.is_authenticated else None
        )
