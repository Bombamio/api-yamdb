from datetime import datetime

from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Avg
from django.utils.text import slugify

# TODO: Не вижу смысла отделять эти модели от моделей в приложении reviews.
# Давайте объединим эти приложения в одно.
MAX_SLUG_LENGTH = 50
MAX_NAME_LENGTH = 256


# TODO: Все модели добавим в админку.
class SlugAutoFillMixin:
    # TODO: Вспомогательный инструмент уберем в отдельный файл.
    '''Миксин для автоматического заполнения slug.'''
    # TODO: Тут и ниже:
    # В докстрингах всегда используются тройные двойные кавычки: """ ... """

    def save(self, *args, **kwargs):
    # Отлично: Доп. функционал
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
# TODO: Модели категорий и жанров очень похожи. Чтобы не дублировать
# настройки полей, создадим абстрактную модель, где прописать эти
# настройки, и будем наследоваться от нее.
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


def validate_year(value):
# TODO: Валидаторы тоже убираем в отдельный файл.
    if value > datetime.now().year:
        raise ValidationError(
            'Год не может быть больше текущего'
        )

# Можно лучше: Лучше привыкать возвращать из валидаторов проверяемое
# значение, если проверка прошла успешно. В случае с функцией это не
# критично, не если не сделать это в валидирующем методе, получим ошибку.

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
    # TODO: Давайте подберем более подходящий тип поля.
    # Учтем, что в нем хранятся маленькие числа.
        "Год издания",
        validators=[validate_year]
    )
    description = models.TextField("Описание", null=True, blank=True)

    @property
    def rating(self):
    # TODO: Такой подход породит множество запросов в БД (отдельный
    # запрос для каждого элемента QuerySet).
    # Нужно изменить подход: добавьте атрибут rating для всех элементов
    # QuerySet путем его аннотирования во вью.
    # Документация для annotate и для Avg
    # https://docs.djangoproject.com/en/4.1/ref/models/querysets/#django.db.models.query.QuerySet.annotate
    # https://docs.djangoproject.com/en/5.1/ref/models/querysets/#avg
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
# TODO: Лишняя модель.
# С созданием промежуточной таблицы для м2м связи Django справится
# самостоятельно.
# Такие модели имеет смысл прописывать, когда мы хотим расширить
# промежуточную таблицу или еще каким-то образом ее донастроить.
# В данном проекте особого смысла объявлять ее явно нет.
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
