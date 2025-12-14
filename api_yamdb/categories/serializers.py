from datetime import datetime

from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.conf import settings

from .utils import calculate_title_rating
from .models import Category, Genre, Title


class CategorySerializer(serializers.ModelSerializer):
    '''Сериализатор для категорий.'''

    slug = serializers.SlugField(
        max_length=settings.MAX_LENGTH_SLUG,
        validators=[
            UniqueValidator(queryset=Category.objects.all())
        ]
    )  # Добавлена проверка уникальности и макс длины.

    class Meta:
        model = Category
        fields = ('name', 'slug')
        read_only_fields = ('slug',)


class GenreSerializer(serializers.ModelSerializer):
    '''Сериализатор для жанров.'''

    class Meta:
        model = Genre
        fields = ('id', 'name', 'slug')
        read_only_fields = ('slug',)


class TitleSerializer(serializers.ModelSerializer):
    '''Сериализатор для произведений.'''
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug'
    )
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(),
        slug_field='slug',
        many=True
    )
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Title
        fields = (
            'id', 'name', 'year', 'description',
            'category', 'genre', 'rating'
        )
        read_only_fields = ('category', 'genre')

    def get_rating(self, obj):
        return calculate_title_rating(obj)

    def validate_year(self, value):
        '''Проверка года выпуска.'''
        current_year = datetime.now().year
        if value > current_year:
            raise serializers.ValidationError(
                'Нельзя добавлять произведение, которое еще не вышло.'
            )
        return value
