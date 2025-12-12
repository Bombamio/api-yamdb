from django.db import models
from django.db.models import Avg
from django.utils.text import slugify


class Category(models.Model):
    '''
    Категории (типы) произведений («Фильмы», «Книги», «Музыка»).
    Одно произведение может быть привязано только к одной категории.

    Поля: `name`, `slug`.
    '''
    name = models.CharField("Название категории", max_length=256)
    slug = models.SlugField("Слаг", unique=True, max_length=50, blank=True)

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # Автоматически генерирует slug из name.
        if not self.slug:
            base_slug = slugify(self.name)
            slug = slugify(self.name)
            counter = 1
            # В цикле проверяет на уникальноть slug.
            while Genre.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            # Автоматически формировать уникальные slug даже при
            # одинаковых названиях.
            self.slug = slug
        super().save(*args, **kwargs)


class Genre(models.Model):
    '''
    Жанры произведений. Одно произведение может быть привязано
    к нескольким жанрам.

    Поля: `name`, `slug`.
    '''
    name = models.CharField("Название жанра", max_length=256)
    slug = models.SlugField("Слаг", unique=True, max_length=50, blank=True)

    class Meta:
        verbose_name = 'жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # Автоматически генерирует slug из name.
        if not self.slug:
            base_slug = slugify(self.name)
            slug = slugify(self.name)
            counter = 1
            # В цикле проверяет на уникальноть slug.
            while Genre.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            # Автоматически формировать уникальные slug даже при
            # одинаковых названиях.
            self.slug = slug
        super().save(*args, **kwargs)


class Title(models.Model):
    '''
    Произведения, к которым пишут отзывы (определённый фильм, книга
    или песенка).

    Поля: `name`, `year`, `description`, `category`, `genre`, `rating`.
    '''
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
    name = models.CharField("Название произведения", max_length=256)
    year = models.IntegerField("Год издания")
    description = models.TextField("Описание", null=True, blank=True)

    @property
    def rating(self):
        '''Вычисляет рейтинг произведения.'''
        avg = self.reviews.aggregate(Avg('score'))['score__avg']
        return int(round(avg)) if avg else None

    class Meta:
        verbose_name = 'произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name


class GenreTitle(models.Model):
    '''
    Класс для поля типа ManyToMany.
    '''
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

    def __str__(self):
        return f'{self.title.name} - {self.genre.name}'

    class Meta:
        # Проверка на отсутствие дублированияполей `genre` и `title`.
        constraints = [
            models.UniqueConstraint(
                fields=["genre", "title"],
                name='unique_genre_title'
            )
        ]
