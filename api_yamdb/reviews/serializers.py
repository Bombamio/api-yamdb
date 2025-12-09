from rest_framework import serializers
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from .models import Review, Comment


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
        extra_kwargs = {
            # title передаётся через контекст, а не в JSON
            'title': {'write_only': True}
        }

    def validate(self, data):
        '''Проверка: один пользователь - один отзыв на произведение'''
        request = self.context.get('request')
        view = self.context.get('view')

        if request and request.method == 'POST' and view:
            # Получаем title из контекста (передаётся в perform_create)
            title = view.kwargs.get('title_id')
            user = request.user

            if not user.is_authenticated:
                raise ValidationError("Требуется аутентификация")

            # Проверяем, есть ли уже отзыв от этого пользователя на это произведение
            if Review.objects.filter(title_id=title, author=user).exists():
                raise ValidationError(
                    "Вы уже оставляли отзыв на это произведение."
                )

        return data

    def validate_score(self, value):
        '''Валидация оценки (1-10)'''
        if not 1 <= value <= 10:
            raise serializers.ValidationError("Оценка должна быть от 1 до 10.")
        return value


class CommentSerializer(serializers.ModelSerializer):
    '''Сериализатор для комментариев (согласно redoc.yaml)'''
    author = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date', 'review')
        read_only_fields = ('id', 'author', 'pub_date')
        extra_kwargs = {
            'review': {'write_only': True}  # review передаётся через контекст
        }
