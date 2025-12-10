# api_yamdb/users/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator


USERNAME_PATTERN = r'^[\w.@+-]+\Z'


class User(AbstractUser):
    '''Кастомизированная модель пользователя для YaMDb.'''

    ROLE_USER = 'user'
    ROLE_MODERATOR = 'moderator'
    ROLE_ADMIN = 'admin'

    ROLE_CHOICES = [
        (ROLE_USER, 'Пользователь'),
        (ROLE_MODERATOR, 'Модератор'),
        (ROLE_ADMIN, 'Администратор'),
    ]

    username_validator = RegexValidator(
        regex=USERNAME_PATTERN,
        message='Имя пользователя может содержать только буквы, '
        'цифры и @/./+/-/_'
    )

    username = models.CharField(
        'Имя пользователя',
        max_length=150,
        unique=True,
        validators=[username_validator],
        help_text='Требуется. 150 символов или меньше.'
        'Только буквы, цифры и @/./+/-/_.'
    )

    email = models.EmailField(
        'Электронная почта',
        max_length=254,
        unique=True,
        help_text='Требуется. Уникальный email.'
    )

    first_name = models.CharField('Имя', max_length=150, blank=True)
    last_name = models.CharField('Фамилия', max_length=150, blank=True)
    bio = models.TextField('Биография', blank=True)

    role = models.CharField(
        'Роль',
        max_length=20,
        choices=ROLE_CHOICES,
        default=ROLE_USER,
        help_text='Роль определяет права доступа'
    )

    confirmation_code = models.CharField(
        'Код подтверждения',
        max_length=100,
        blank=True,
        null=True,
        editable=False
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ['username']

    def __str__(self):
        return self.username

    @property
    def is_admin(self):
        '''Проверяет, является ли пользователь администратором.'''
        return self.role == self.ROLE_ADMIN or self.is_superuser

    @property
    def is_moderator(self):
        '''Проверяет, является ли пользователь модератором.'''
        return self.role == self.ROLE_MODERATOR
