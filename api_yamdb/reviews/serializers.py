from rest_framework import serializers
from .models import Review, Comment
from django.core.validators import MinValueValidator, MaxValueValidator


class ReviewSerializer(serializers.ModelSerializer):
    '''Сериализатор для отзывов (согласно redoc.yaml)'''
    # Поля из документации
    author = serializers.StringRelatedField(read_only=True)
    score = serializers.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        read_only_fields = ('id', 'author', 'pub_date')

    def validate(self, data):
        '''Проверка уникальности отзыва'''
        # Пока проверяем по title_id/author_id, позже заменим на ForeignKey
        request = self.context.get('request')

        if request and request.method == 'POST':
            title_id = request.parser_context['kwargs'].get('title_id')
            user = request.user

            if Review.objects.filter(
                title_id=title_id,
                author_id=user.id if user.is_authenticated else None
            ).exists():
                raise serializers.ValidationError(
                    "Вы уже оставляли отзыв на это произведение."
                )

        return data


class CommentSerializer(serializers.ModelSerializer):
    '''Сериализатор для комментариев (согласно redoc.yaml)'''
    author = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date')
        read_only_fields = ('id', 'author', 'pub_date')
