from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth import get_user_model

from categories.models import Title
User = get_user_model()
# TODO: Стоит добавить одну пустую строку после импортов.


# TODO: Давайте все модели добавим в админку.
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
