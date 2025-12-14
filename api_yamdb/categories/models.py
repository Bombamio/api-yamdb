from django.db import models
from django.utils.text import slugify
from django.core.validators import MaxValueValidator
from django.db.models import Avg
from datetime import datetime

# TODO Проблема: datetime.now().year вычисляется при импорте модуля
# (при запуске сервера) и не обновляется.
# В 2025 году нельзя будет добавить произведение 2024 года!

MAX_SLUG_LENGTH = 50
MAX_NAME_LENGTH = 256


class SlugAutoFillMixin:
    '''Миксин для автоматического заполнения slug.'''

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1

            # Используем self.__class__ чтобы работало для любых моделей
            while self.__class__.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)


class Category(SlugAutoFillMixin, models.Model):
    '''Категории (типы) произведений («Фильмы», «Книги», «Музыка»).'''
    name = models.CharField(
        "Название категории", max_length=MAX_NAME_LENGTH, unique=True
    )
    slug = models.SlugField(
        "Слаг",
        unique=True,
        max_length=MAX_SLUG_LENGTH,
        blank=True
    )

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['name']

    def __str__(self):
        return self.name


class Genre(SlugAutoFillMixin, models.Model):
    '''Жанры произведений.'''
    name = models.CharField("Название жанра", max_length=MAX_NAME_LENGTH)
    slug = models.SlugField(
        "Слаг", unique=True, max_length=MAX_SLUG_LENGTH, blank=True
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
        verbose_name="Категория",
        null=True,
        blank=True
    )
    genre = models.ManyToManyField(
        Genre,
        through='GenreTitle',
        verbose_name="Жанры",
        related_name='titles',
    )
    name = models.CharField(
        "Название произведения", max_length=MAX_NAME_LENGTH
    )
    year = models.IntegerField(
        "Год издания",
        validators=[MaxValueValidator(
            limit_value=lambda: datetime.now().year,
            message='Год не может быть больше текущего'
        )]
    )
    description = models.TextField("Описание", null=True, blank=True)

    @property
    def rating(self):
        '''Вычисляет рейтинг произведения.'''
        avg = self.reviews.aggregate(Avg('score'))['score__avg']
        return round(avg, 1) if avg else None  # Округление до 0.1

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'
        ordering = ['name']

    def __str__(self):
        return self.name


class GenreTitle(models.Model):
    '''Класс для поля типа ManyToMany.'''
    genre = models.ForeignKey(
        Genre,
        on_delete=models.CASCADE,
        related_name='genre_titles',
        verbose_name="Жанры",
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='genre_titles',
        verbose_name="Произведения",
    )

    class Meta:
        verbose_name = 'Жанр произведения'
        verbose_name_plural = 'Жанры произведений'
        constraints = [
            models.UniqueConstraint(
                fields=["genre", "title"],
                name='unique_genre_title'
            ),
        ]

    def __str__(self):
        return f'{self.title.name} - {self.genre.name}'
