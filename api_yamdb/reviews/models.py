from django.contrib.auth import get_user_model
from django.db import models

from categories.models import Title

User = get_user_model()


class Review(models.Model):
    text = models.TextField()
    score = models.IntegerField()   # [1 .. 10]
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reviews'
    )
    pub_date = models.DateTimeField(auto_now_add=True, db_index=True)
    # Не уверен нужно ли добавлять поле title.
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name='reviews'
    )


class Comment(models.Model):
    text = models.TextField()
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reviews'
    )
    pub_date = models.DateTimeField(auto_now_add=True, db_index=True)
    # Не уверен нужно ли добавлять поле title.
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name='comments'
    )
    # Не уверен нужно ли добавлять поле review.
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name='comments'
    )
