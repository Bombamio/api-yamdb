from django.db.models import Avg
from rest_framework import serializers
from datetime import date
import re

from .models import Category, Genre, Title


def get_current_year():
    '''Функция для получения текущего года.'''
    return date.today().year


class SlugSerializer(serializers.ModelSerializer):
    '''Базовый сериализатор для моделей со slug.'''

    class Meta:
        abstract = True

    def validate_slug(self, value):
        '''Валидация slug.'''
        if not value:
            return value

        if len(value) > 50:
            raise serializers.ValidationError(
                'Slug не может быть длиннее 50 символов.'
            )

        if not re.match(r'^[-a-zA-Z0-9_]+$', value):
            raise serializers.ValidationError(
                'Slug может содержать только буквы, цифры, дефисы и _.'
                'Текущее значение: {}'.format(value)
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
        '''Вычисляет рейтинг произведения.'''
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
        current_year = get_current_year()
        if not 1000 <= value <= current_year:
            raise serializers.ValidationError(
                f'Год должен быть в диапазоне от 1000 до {current_year}.'
            )
        return value

    def _handle_genres(self, instance, genres_data):
        '''Обработка жанров (вынесен в отдельный метод).'''
        if genres_data is not None:
            instance.genre.clear()
            instance.genre.add(*genres_data)

    def create(self, validated_data):
        '''Создание произведения с жанрами.'''
        genres_data = validated_data.pop('genre', [])
        title = Title.objects.create(**validated_data)
        self._handle_genres(title, genres_data)
        return title

    def update(self, instance, validated_data):
        '''Обновление произведения с жанрами.'''
        genres_data = validated_data.pop('genre', None)

        # Обновляем поля более эффективно
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        self._handle_genres(instance, genres_data)
        return instance

    def to_representation(self, instance):
        '''Используем сериализатор для чтения при выводе.'''
        return TitleReadSerializer(instance, context=self.context).data
