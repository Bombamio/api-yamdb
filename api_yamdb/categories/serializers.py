from django.db.models import Avg
from rest_framework import serializers
from datetime import datetime
import re

from .models import Category, Genre, Title


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
        # НЕ добавляем read_only_fields для slug!
        # Slug должен быть доступен для записи при создании


class GenreSerializer(SlugSerializer):
    '''Сериализатор для жанров.'''

    class Meta:
        model = Genre
        fields = ('name', 'slug')
        # НЕ добавляем read_only_fields для slug!


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
