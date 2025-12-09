from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'

    CHOICES = [
        (USER, 'User',),
        (MODERATOR, 'Moderator',),
        (ADMIN, 'Admin',),
    ]

    role = models.CharField(
        max_length=20,
        choices=CHOICES,
        default=USER
    )

    @property
    def is_admin(self):
        """
        Админ — тот, кто либо имеет роль admin, либо является суперпользователем.
        """
        return self.role == self.ADMIN or self.is_superuser

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR
    
    def __str__(self):
        return self.username
