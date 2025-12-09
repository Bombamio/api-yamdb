from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator


class User(AbstractUser):
    '''Кастомизированная модель пользователя для YaMDb.'''

    username_validator = RegexValidator(
        regex=r'^[\w.@+-]+\Z',
        message='Имя пользователя может содержать только буквы, цифры и @/./+/-/_'
    )

    username = models.CharField(
        'Имя пользователя',
        max_length=150,
        unique=True,
        validators=[username_validator],
        help_text='Обязательное поле. Не более 150 символов. Только буквы, цифры и @/./+/-/_.'
    )

    email = models.EmailField(
        'Электронная почта',
        max_length=254,
        unique=True,
        help_text='Обязательное поле. Уникальный email.'
    )

    first_name = models.CharField('Имя', max_length=150, blank=True)
    last_name = models.CharField('Фамилия', max_length=150, blank=True)
    bio = models.TextField('Биография', blank=True)

    ROLE_CHOICES = [
        ('user', 'Пользователь'),
        ('moderator', 'Модератор'),
        ('admin', 'Администратор'),
    ]

    role = models.CharField(
        'Роль',
        max_length=20,
        choices=ROLE_CHOICES,
        default='user',
        help_text='Роль определяет права доступа пользователя'
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
        return self.role == 'admin' or self.is_superuser

    @property
    def is_moderator(self):
        return self.role == 'moderator'
