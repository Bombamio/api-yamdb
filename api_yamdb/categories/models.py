from django.contrib.auth import get_user_model
from django.db import models

# TODO: Добавь verbose_name далее в проекте
# TODO: Допиши докстринги
# TODO: В GenreTitle два одинаковых поля 'genre' (строка 36-39). Должно быть: title и genre.
# TODO: При удалении категории произведения не должны удаляться - используй on_delete=models.SET_NULL.
# TODO: Добавить Meta-классы для всех моделей
# TODO: Нет UniqueConstraint в GenreTitle - могут быть дубли связей
User = get_user_model()


class Category(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(unique=True, max_length=50)

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(unique=True, max_length=50)

    def __str__(self):
        return self.name


class Title(models.Model):
    # TODO может лучше так "category":
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,  # При удалении категории произведение остаётся!
        null=True,
        blank=True,
        related_name='titles',  # category.titles.all()
        verbose_name='Категория'
    )

    genre = models.ManyToManyField(
        Genre, through='GenreTitle'
        # TODO : ,related_name='titles', verbose_name='Жанры'
    )
    name = models.CharField(max_length=256)
    year = models.IntegerField()
    description = models.TextField(null=True, blank=True)

    # NOTE: Далее важно для моей части
    rating = models.IntegerField(
        null=True,
        blank=True,
        verbose_name='Рейтинг',
        help_text='Средняя оценка от 1 до 10 (рассчитывается автоматически)'
    )

    def __str__(self):
        return self.name


class GenreTitle(models.Model):
    # TODO: Дублирование поля в GenreTitle исправил genre на title
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE
    )
    genre = models.ForeignKey(
        Genre, on_delete=models.CASCADE
    )

    # TODO: Добавь  related_name и verbose_name в GenreTitle
    # TODO: class Meta:
    def __str__(self):
        return f'{self.title.name} - {self.genre.name}'
