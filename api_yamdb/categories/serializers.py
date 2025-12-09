from rest_framework import serializers
from api_yamdb.utils import calculate_title_rating
from .models import Category, Genre, Title


class CategorySerializer(serializers.ModelSerializer):
    pass


class GenreSerializer(serializers.ModelSerializer):
    pass


class TitleSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(many=True, read_only=True)
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Title
        fields = (
            'id', 'name', 'year', 'description',
            'category', 'genre', 'rating'
        )

    def get_rating(self, obj):
        return calculate_title_rating(obj)
