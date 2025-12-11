from datetime import datetime

from rest_framework import serializers

from .utils import calculate_title_rating
from .models import Category, Genre, Title


class CategorySerializer(serializers.ModelSerializer):
    '''Сериализатор для категорий.'''

    class Meta:
        model = Category
        fields = ('id', 'name', 'slug')
        read_only_fields = ('slug',)


class GenreSerializer(serializers.ModelSerializer):
    '''Сериализатор для жанров.'''

    class Meta:
        model = Genre
        fields = ('id', 'name', 'slug')
        read_only_fields = ('slug',)


class TitleSerializer(serializers.ModelSerializer):
    '''Сериализатор для произведений.'''
    category = serializers.SlugRelatedField(slug_field='slug')
    genre = serializers.SlugRelatedField(many=True, slug_field='slug')
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Title
        fields = (
            'id', 'name', 'category', 'genre', 'year', 'description',
            'rating'
        )
        read_only_fields = ('category', 'genre')

    def get_rating(self, obj):
        return calculate_title_rating(obj)

    def validate_year(self, value):
        """Проверка года выпуска."""
        current_year = datetime.now().year
        if value > current_year:
            raise serializers.ValidationError(
                'Нельзя добавлять произведение, которое еще не вышло.'
            )
        return value
