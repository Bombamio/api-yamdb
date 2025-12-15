from django.db import models
from django.utils.text import slugify
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models import Avg
from datetime import date

# TODO Проблема: datetime.now().year вычисляется при импорте модуля
# (при запуске сервера) и не обновляется.
# В 2025 году нельзя будет добавить произведение 2024 года!

MAX_SLUG_LENGTH = 50
MAX_NAME_LENGTH = 256
CURRENT_YEAR = date.today().year


def get_current_year():
    '''Функция для получения текущего года.'''
    return date.today().year


class SlugAutoFillMixin:
    '''Миксин для автоматического заполнения slug.'''

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1

            while self.__class__.objects.filter(slug=slug).exists():
                slug = f'{base_slug}-{counter}'
                counter += 1
            self.slug = slug[:MAX_SLUG_LENGTH]
        super().save(*args, **kwargs)


class Category(SlugAutoFillMixin, models.Model):
    '''Категории (типы) произведений («Фильмы», «Книги», «Музыка»).'''
    name = models.CharField(
        'Название категории',
        max_length=MAX_NAME_LENGTH,
        unique=True,
        help_text='Например: Фильмы, Книги, Музыка'
    )
    slug = models.SlugField(
        'Слаг',
        unique=True,
        max_length=MAX_SLUG_LENGTH,
        blank=True,
        help_text='URL-идентификатор категории'
    )

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['name']

    def __str__(self):
        return self.name


class Genre(SlugAutoFillMixin, models.Model):
    '''Жанры произведений.'''
    name = models.CharField(
        'Название жанра',
        unique=True,
        max_length=MAX_NAME_LENGTH,
        help_text='Например: Драма, Комедия, Фантастика' 
    )
    slug = models.SlugField(
        'Слаг',
        unique=True,
        max_length=MAX_SLUG_LENGTH,
        blank=True,
        help_text='URL-идентификатор жанра'
    )

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'
        ordering = ['name']

    def __str__(self):
        return self.name


class Title(models.Model):
    '''Произведения, к которым пишут отзывы'''
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name='titles',
        verbose_name='Категория',
        null=True,
        blank=True,
        help_text='Выберите категорию произведения'
    )
    genre = models.ManyToManyField(
        Genre,
        through='GenreTitle',
        verbose_name='Жанры',
        related_name='titles',
        blank=True,
        help_text='Выберите жанры произведения'
    )
    name = models.CharField(
        'Название произведения',
        max_length=MAX_NAME_LENGTH,
        help_text='Полное название произведения'
    )
    year = models.IntegerField(
        'Год выпуска',
        validators=[
            MinValueValidator(
                limit_value=1000,  # Минимальный разумный год
                message='Год не может быть меньше 1000'
            ),
            MaxValueValidator(
                limit_value=get_current_year,
                message='Год не может быть больше текущего'
            )
        ],
        help_text=f'Год выпуска произведения (не позднее {get_current_year()})'
    )
    description = models.TextField(
        'Описание',
        null=True,
        blank=True,
        help_text='Подробное описание произведения'
    )
    created_at = models.DateTimeField(
        'Дата создания',
        auto_now_add=True,
        editable=False
    )
    updated_at = models.DateTimeField(
        'Дата обновления',
        auto_now=True,
        editable=False
    )

    @property
    def rating(self):
        '''Вычисляет рейтинг произведения.'''
        avg = self.reviews.aggregate(Avg('score'))['score__avg']
        return round(avg, 1) if avg is not None else None

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'
        ordering = ['-created_at', 'name']

    def __str__(self):
        return f'{self.name} ({self.year})'


class GenreTitle(models.Model):
    '''Связь ManyToMany между произведениями и жанрами.'''
    genre = models.ForeignKey(
        Genre,
        on_delete=models.CASCADE,
        related_name='genre_titles',
        verbose_name='Жанр',
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='genre_titles',
        verbose_name='Произведение',
    )
    created_at = models.DateTimeField(
        'Дата создания',
        auto_now_add=True,
        editable=False
    )

    class Meta:
        verbose_name = 'Жанр произведения'
        verbose_name_plural = 'Жанры произведений'
        constraints = [
            models.UniqueConstraint(
                fields=['genre', 'title'],
                name='unique_genre_title'
            ),
        ]
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.title.name} - {self.genre.name}'
