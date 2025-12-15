from datetime import datetime
import re

from django.db.models import Avg
from rest_framework import serializers

from categories.models import Category, Genre, Title
from reviews.models import Comment, Review


# Categories fields.

class SlugSerializer(serializers.ModelSerializer):
    # TODO:Лишний класс.
    # Все валадации модельный сериализатор подтянет из модели.
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
    # TODO: Во всем проекте:
    # В докстрингах всегда используются тройные двойные кавычки: """ ... """

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
    # TODO: Для этого поля не нужен метод. Используем обычный IntegerField,
    # задав значение по умолчанию (в соответствии со спецификацией - None).
    # Вычислять рейтинг мы будем в кверисете при настройке вьюсета
    # (детали в комментарии к модели к полю rating)
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
        # TODO: Лишняя строка.
        # id - автозаполняемое поле, а поля rating вообще не будет в модели.

    def get_rating(self, obj):
        # TODO: Лишний метод.
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
        # TODO: Чтобы запрос без жанров не прошел валидацию надо
        # добавить два параметра для этого поля: allow_null и allow_empty.
        # Значением для обоих будет False.
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
        # TODO: Валидация подтянется из настроек поля в модели.
        '''Проверка года выпуска.'''
        current_year = datetime.now().year
        if value > current_year:
            raise serializers.ValidationError(
                'Нельзя добавлять произведение, которое еще не вышло.'
            )
        return value
# TODO: Этот и следующий метод лишние.

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

# TODO: Чтобы получить ответ, соответствующий спецификации, надо
# переопределить метод to_representation, в котором передать созданный
# объект в сериализатор для чтения произведений и вернуть атрибут data
# получившегося объекта сериализатора.


# Review fields.

class ReviewSerializer(serializers.ModelSerializer):
    '''Сериализатор для отзывов.'''
    author = serializers.StringRelatedField(read_only=True)
    # TODO: Неудачный выбор типа. Фактически тебе случайно повезло, что
    # он подходит, так как мы не контролируем преобразование в строку для
    # объектов типа User. Нужен другой.
    # Посмотри в сторону SlugRelatedField. У него можно явно указать из
    # какого поля брать значение.
    score = serializers.IntegerField(
        # TODO: Это поле явно прописывать не надо. Настройки подтянется
        # из модели.
        min_value=1,
        max_value=10,
        help_text="Оценка от 1 до 10"
    )

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        read_only_fields = ('id', 'author', 'pub_date')
        # TODO: Лишняя строка.
        # id и pub_date являются автозаполняемыми и доступны только для
        # чтения по умолчанию, а для поля автор соответствующее свойство
        # мы включили в 134 строке.


class CommentSerializer(serializers.ModelSerializer):
    '''Сериализатор для комментариев.'''
    author = serializers.StringRelatedField(read_only=True)
    # TODO: См. комментарий к 155 строке

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date')
        read_only_fields = ('id', 'author', 'pub_date')
        # TODO: Лишняя строка.
        extra_kwargs = {
            'text': {'help_text': 'Текст комментария'}
        }
