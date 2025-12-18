from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from . import constants
from .mixins import SlugAutoFillMixin
from .validators import validate_year


User = get_user_model()


# Categories fields.

class AbstractBaseModel(SlugAutoFillMixin, models.Model):
    """Абстрактная модель для Category и Genre."""
    name = models.CharField(
        "Название", max_length=constants.MAX_NAME_LENGTH, unique=True
    )
    slug = models.SlugField(
        "Слаг",
        unique=True,
        max_length=constants.MAX_SLUG_LENGTH,
        blank=True
    )

    class Meta:
        abstract = True
        ordering = ['name']

    def __str__(self):
        return self.name


class Category(AbstractBaseModel):
    """Категории (типы) произведений («Фильмы», «Книги», «Музыка»)."""

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Genre(AbstractBaseModel):
    """Жанры произведений."""

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


class Title(models.Model):
    """Произведения, к которым пишут отзывы"""
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
        verbose_name="Жанры",
        related_name='titles',
    )
    name = models.CharField(
        "Название произведения", max_length=constants.MAX_NAME_LENGTH
    )
    year = models.PositiveSmallIntegerField(
        "Год издания",
        validators=[validate_year]
    )
    description = models.TextField("Описание", null=True, blank=True)

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'
        ordering = ['name']

    def __str__(self):
        return self.name


# Reviews fields.

class Review(models.Model):
    """
    Отзывы на произведения. Отзыв привязан к определённому произведению.

    Поля: `text`, `score`, `author`, `pub_date`, `title`.
    """
    text = models.TextField('Текст отзыва')
    score = models.PositiveSmallIntegerField(
        'Оценка произвидения',
        validators=[
            MinValueValidator(constants.MIN_VALUE),
            MaxValueValidator(constants.MAX_VALUE)
        ],
        help_text=f'Оценка от {constants.MIN_VALUE} до {constants.MAX_VALUE}'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name="Автор отзыва"
    )
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True,
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Произведение'
    )

    class Meta:
        # Один пользователь - один отзыв на произведение
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'author'],
                name='unique_review_per_title_and_author'
            )
        ]
        verbose_name = 'отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ['-pub_date']


class Comment(models.Model):
    """
    Комментарии к отзывам. Комментарий привязан к определённому отзыву.

    Поля: `text`, `author`, `pub_date`, `review`.
    """
    text = models.TextField(
        'Текст комментария',
        help_text='Текст комментария'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор комментария'
    )
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True,
    )
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Отзыв'
    )

    class Meta:
        verbose_name = 'коментарий'
        verbose_name_plural = 'Коментарии'
        ordering = ['pub_date']

    def __str__(self):
        return f'Комментарий {self.id} к отзыву {self.review.id}'
