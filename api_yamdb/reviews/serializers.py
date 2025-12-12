from rest_framework import serializers
from .models import Review, Comment


class ReviewSerializer(serializers.ModelSerializer):
    '''Сериализатор для отзывов.'''
    # Поля из документации
    author = serializers.StringRelatedField(read_only=True)
    score = serializers.IntegerField(
        min_value=1,
        max_value=10,
        help_text='Оценка от 1 до 10'
    )

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        read_only_fields = ('id', 'author', 'pub_date')


class CommentSerializer(serializers.ModelSerializer):
    '''Сериализатор для комментариев.'''
    author = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date')
        read_only_fields = ('id', 'author', 'pub_date')
        extra_kwargs = {
            'text': {'help_text': 'Текст комментария'}
        }
