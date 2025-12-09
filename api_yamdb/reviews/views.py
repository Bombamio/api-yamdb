from rest_framework import viewsets, permissions
from django.shortcuts import get_object_or_404
from .models import Review, Comment
from categories.models import Title
from .serializers import ReviewSerializer, CommentSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    '''ViewSet для отзывов'''
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        '''Получаем отзывы для конкретного произведения'''
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        return Review.objects.filter(title=title)

    def perform_create(self, serializer):
        '''Создание отзыва с автором'''
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)

        # Используем ForeignKey author и title из моделей Ильи
        serializer.save(
            author=self.request.user,
            title=title
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

        # Используем ForeignKey author из моделей Ильи
        serializer.save(
            review=review,
            author=self.request.user
        )
