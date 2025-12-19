from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.text import slugify

from . import constants
from .validators import validate_year


User = get_user_model()


# Categories fields.

class NamedSlugModel(models.Model):
    """Абстрактная модель с полями name и slug, для Category и Genre."""
    name = models.CharField(
        "Название", max_length=constants.MAX_NAME_LENGTH, unique=True
    )
    slug = models.SlugField(
        "Слаг",
        unique=True,
        max_length=constants.MAX_SLUG_LENGTH,
        blank=True
    )

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

    class Meta:
        abstract = True
        ordering = ['name']

    def __str__(self):
        return self.name


class Category(NamedSlugModel):
    """Категории (типы) произведений («Фильмы», «Книги», «Музыка»)."""

    class Meta(NamedSlugModel.Meta):
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Genre(NamedSlugModel):
    """Жанры произведений."""

    class Meta(NamedSlugModel.Meta):
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
    year = models.SmallIntegerField(
        "Год издания",
        validators=[validate_year]
    )
    description = models.TextField("Описание", blank=True)

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
