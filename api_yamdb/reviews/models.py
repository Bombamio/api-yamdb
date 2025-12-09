from django.contrib.auth import get_user_model
from django.db import models

from categories.models import Title

User = get_user_model()


class Review(models.Model):
    """
    Отзывы на произведения. Отзыв привязан к определённому произведению.
    
    Поля: `text`, `score`, `author`, `pub_date`, `title`.
    """
    text = models.TextField("Текст отзыва")
    score = models.IntegerField("Оценка произвидения")   # [1 .. 10]
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name="Автор отзыва"
    )
    pub_date = models.DateTimeField(
        "Дата публикации",
        auto_now_add=True,
        db_index=True
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name="Произведение"
    )

    class Meta:
        ordering = ('pub_date',)


class Comment(models.Model):
    """
    Комментарии к отзывам. Комментарий привязан к определённому отзыву.

    Поля: `text`, `author`, `pub_date`, `review`.
    """
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
        db_index=True
    )
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name="Отзыв"
    )

    class Meta:
        ordering = ('pub_date',)
