from rest_framework import viewsets, permissions
from django.shortcuts import get_object_or_404
from categories.models import Title

from .models import Review, Comment
from .serializers import ReviewSerializer, CommentSerializer
from api.permissions import IsAuthorOrModeratorOrAdminOrReadOnly


class ReviewViewSet(viewsets.ModelViewSet):
    '''ViewSet для отзывов'''
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_title(self):
        '''Получаем произведение по ID из URL'''
        return get_object_or_404(Title, id=self.kwargs.get('title_id'))

    def get_queryset(self):
        '''Получаем отзывы для конкретного произведения'''
        return Review.objects.filter(title=self.get_title())

    def perform_create(self, serializer):
        '''Создание отзыва с автором и произведением'''
        serializer.save(
            author=self.request.user,
            title=self.get_title()
        )


class CommentViewSet(viewsets.ModelViewSet):
    '''ViewSet для комментариев к отзывам'''
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

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
