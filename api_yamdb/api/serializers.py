from datetime import datetime
import re

from django.db.models import Avg
from rest_framework import serializers

from categories.models import Category, Genre, Title
from reviews.models import Comment, Review



# Categories fields.

class SlugSerializer(serializers.ModelSerializer):
    '''Базовый сериализатор для моделей со slug.'''

    class Meta:
        abstract = True

    def validate_slug(self, value):
        if not value:
            return value

        if len(value) > 50:
            raise serializers.ValidationError(
                'Slug не может быть длиннее 50 символов.'
            )

        if not re.match(r'^[-a-zA-Z0-9_]+$', value):
            raise serializers.ValidationError(
                'Slug может содержать только буквы, цифры, дефисы и _.'
            )

        return value


class CategorySerializer(SlugSerializer):
    '''Сериализатор для категорий.'''

    class Meta:
        model = Category
        fields = ('name', 'slug')


class GenreSerializer(SlugSerializer):
    '''Сериализатор для жанров.'''

    class Meta:
        model = Genre
        fields = ('name', 'slug')


class TitleReadSerializer(serializers.ModelSerializer):
    '''Сериализатор для просмотра произведений.'''
    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(many=True, read_only=True)
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Title
        fields = (
            'id', 'name', 'year', 'rating', 'description',
            'genre', 'category'
        )
        read_only_fields = ('id', 'rating')

    def get_rating(self, obj):
        avg = obj.reviews.aggregate(Avg('score'))['score__avg']
        return round(avg, 1) if avg else None  # Округление до 0.1


class TitleWriteSerializer(serializers.ModelSerializer):
    '''Сериализатор для добавления произведений.'''
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all(),
        required=False,
        allow_null=True
    )
    genre = serializers.SlugRelatedField(
        slug_field='slug',
        many=True,
        queryset=Genre.objects.all()
    )

    class Meta:
        model = Title
        fields = (
            'id', 'name', 'year', 'description',
            'genre', 'category'
        )

    def validate_year(self, value):
        '''Проверка года выпуска.'''
        current_year = datetime.now().year
        if value > current_year:
            raise serializers.ValidationError(
                'Нельзя добавлять произведение, которое еще не вышло.'
            )
        return value

    def create(self, validated_data):
        # Извлекаем жанры из validated_data
        genres_data = validated_data.pop('genre', [])
        title = Title.objects.create(**validated_data)

        # Добавляем жанры через промежуточную модель
        for genre in genres_data:
            title.genre.add(genre)

        return title

    def update(self, instance, validated_data):
        # Извлекаем жанры из validated_data
        genres_data = validated_data.pop('genre', None)

        # Обновляем поля
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Обновляем жанры если они переданы
        if genres_data is not None:
            instance.genre.clear()
            for genre in genres_data:
                instance.genre.add(genre)

        return instance


# Review fields.

class ReviewSerializer(serializers.ModelSerializer):
    '''Сериализатор для отзывов.'''
    author = serializers.StringRelatedField(read_only=True)
    score = serializers.IntegerField(
        min_value=1,
        max_value=10,
        help_text="Оценка от 1 до 10"
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
