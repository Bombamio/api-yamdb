from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth import get_user_model

from .mixins import SlugAutoFillMixin
from .validators import validate_year


MAX_SLUG_LENGTH = 50
MAX_NAME_LENGTH = 256

User = get_user_model()


# Categories fields.

class AbstractBaseModel(SlugAutoFillMixin, models.Model):
    """Абстрактная модель для Category и Genre."""
    name = models.CharField(
        "Название", max_length=MAX_NAME_LENGTH, unique=True
    )
    slug = models.SlugField(
        "Слаг",
        unique=True,
        max_length=MAX_SLUG_LENGTH,
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
        "Название произведения", max_length=MAX_NAME_LENGTH
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
# TODO: Для всех моделей добавим verbose_name и verbose_name_plural,
# а также метод __str__
    '''
    Отзывы на произведения. Отзыв привязан к определённому произведению.

    Поля: `text`, `score`, `author`, `pub_date`, `title`.
    '''
    # TODO: Тут и ниже:
    # В докстрингах всегда используются тройные двойные кавычки: """ ... """
    text = models.TextField("Текст отзыва")
    score = models.IntegerField(
    # TODO: Подберем более удачный тип поля.
    # Стоит участь, что в данном поле хранятся маленькие положительные числа.
        "Оценка произвидения",
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        # TODO: Все статичные ограничения (макс. длина, границы значения полей)
        # убираем в константы. Для констант в каждом приложении заведем
        # файл - constants.py
        help_text='Оценка от 1 до 10'
        # TODO: Текст сформируем через f-строку, чтобы при изменении
        # границ он автоматически подстраивался.
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name="Автор отзыва"
    )
    pub_date = models.DateTimeField(
        "Дата публикации",
        auto_now_add=True,
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name="Произведение"
    )

    class Meta:
        # Один пользователь - один отзыв на произведение
        constraints = [
            models.UniqueConstraint(
            # Отлично: Верно! Такие ограничения всегда стоит дублировать
            # на уровне БД.
                fields=['title', 'author'],
                name='unique_review_per_title_and_author'
            )
        ]
        ordering = ['-pub_date']


class Comment(models.Model):
    '''
    Комментарии к отзывам. Комментарий привязан к определённому отзыву.

    Поля: `text`, `author`, `pub_date`, `review`.
    '''
    text = models.TextField("Текст комментария")
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name="Автор комментария"
    )
    pub_date = models.DateTimeField(
        "Дата публикации",
        auto_now_add=True,
    )
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name="Отзыв"
    )

    class Meta:
        ordering = ['pub_date']

    def __str__(self):
        return f'Комментарий {self.id} к отзыву {self.review.id}'
