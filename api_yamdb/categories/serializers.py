from rest_framework import serializers
from api_yamdb.utils import calculate_title_rating
from datetime import datetime
from .models import Category, Genre, Title


class CategorySerializer(serializers.ModelSerializer):
    '''Сериализатор для категорий.'''

    class Meta:
        model = Category
        fields = ('id', 'name', 'slug')


class GenreSerializer(serializers.ModelSerializer):
    '''Сериализатор для жанров.'''

    class Meta:
        model = Genre
        fields = ('id', 'name', 'slug')


class TitleSerializer(serializers.ModelSerializer):
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
        read_only_fields = ('rating',)  # rating нельзя менять напрямую

    def get_rating(self, obj):
        return calculate_title_rating(obj)
