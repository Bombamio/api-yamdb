from django.db import models


class Category(models.Model):
    """
    Категории (типы) произведений («Фильмы», «Книги», «Музыка»).
    Одно произведение может быть привязано только к одной категории.

    Поля: `name`, `slug`.
    """
    name = models.CharField("Название категории", max_length=256)
    slug = models.SlugField("Слаг", unique=True, max_length=50)

    def __str__(self):
        return self.name


class Genre(models.Model):
    """
    Жанры произведений. Одно произведение может быть привязано
    к нескольким жанрам.

    Поля: `name`, `slug`.
    """
    name = models.CharField("Название жанра", max_length=256)
    slug = models.SlugField("Слаг", unique=True, max_length=50)

    def __str__(self):
        return self.name


class Title(models.Model):
    """
    Произведения, к которым пишут отзывы (определённый фильм, книга
    или песенка).

    Поля: `name`, `year`, `description`, `category`, `genre`, `rating`.
    """
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

    def __str__(self):
        return self.name


class GenreTitle(models.Model):
    """
    Класс для поля типа ManyToMany.
    """
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
            ),
            models.CheckConstraint(
                check=~models.Q(genre=models.F('title')),
                name='prevent_self_follow'
            )
        ]
