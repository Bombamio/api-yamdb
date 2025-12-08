from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

# ВРЕМЕННЫЕ ЗАГЛУШКИ - позже замените на настоящие ForeignKey


class Review(models.Model):
    """Отзыв на произведение"""
    # Временные заглушки вместо ForeignKey
    title_id = models.IntegerField(
        'ID произведения',
        help_text='ID произведения из базы'
    )
    author_id = models.IntegerField(
        'ID автора',
        help_text='ID пользователя из базы'
    )

    # Основные поля, которые не зависят от моделей Ильи
    text = models.TextField('Текст отзыва')
    score = models.IntegerField(
        'Оценка',
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        help_text='Оценка от 1 до 10'
    )
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True
    )

    class Meta:
        # Один пользователь - один отзыв на произведение
        constraints = [
            models.UniqueConstraint(
                fields=['title_id', 'author_id'],
                name='unique_review_per_title_and_author'
            )
        ]
        ordering = ['-pub_date']

    def __str__(self):
        return f'Отзыв {self.id} на произведение {self.title_id}'


class Comment(models.Model):
    """Комментарий к отзыву"""
    # Связь с отзывом (ваша же модель)
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments'
    )

    # Временная заглушка для автора
    author_id = models.IntegerField('ID автора комментария')

    # Основные поля
    text = models.TextField('Текст комментария')
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True
    )

    class Meta:
        ordering = ['pub_date']

    def __str__(self):
        return f'Комментарий {self.id} к отзыву {self.review.id}'
