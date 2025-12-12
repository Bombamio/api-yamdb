from rest_framework import serializers

from datetime import datetime

from .models import Category, Genre, Title


class CategorySerializer(serializers.ModelSerializer):
    '''Сериализатор для категорий.'''

    class Meta:
        model = Category
        fields = ('name', 'slug')
        read_only_fields = ('slug',)


class GenreSerializer(serializers.ModelSerializer):
    '''Сериализатор для жанров.'''

    class Meta:
        model = Genre
        fields = ('name', 'slug')
        read_only_fields = ('slug',)


class TitleReadSerializer(serializers.ModelSerializer):
    '''Сериализатор для просмотра произведений.'''
    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(many=True, read_only=True)

    class Meta:
        model = Title
        fields = (
            'id', 'name', 'year', 'rating', 'description',
            'genre', 'category'
        )


class TitleWriteSerializer(serializers.ModelSerializer):
    '''Сериализатор для добавления произведений.'''
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all()
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
