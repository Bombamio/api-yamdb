from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.utils.translation import gettext_lazy as _

from . import constants
from .validators import validate_username


class User(AbstractUser):
    """Кастомизированная модель пользователя для YaMDb."""

    class UserRoles(models.TextChoices):
        USER = 'user', _('Пользователь')
        MODERATOR = 'moderator', _('Модератор')
        ADMIN = 'admin', _('Администратор')

    username_validator = UnicodeUsernameValidator(
        message=(
            'Имя пользователя может содержать только буквы, цифры и '
            '@/./+/-/_'
        )
    )

    username = models.CharField(
        'Имя пользователя',
        max_length=constants.MAX_NAME_LENGTH,
        unique=True,
        validators=[username_validator, validate_username],
        help_text=(
            'Требуется. 150 символов или меньше. Только буквы, цифры и '
            '@/./+/-/_'
        )
    )

    email = models.EmailField(
        'Электронная почта',
        max_length=constants.MAX_EMAIL_LENGTH,
        unique=True,
        help_text='Требуется. Уникальный email.'
    )

    first_name = models.CharField(
        'Имя', max_length=constants.MAX_NAME_LENGTH, blank=True
    )
    last_name = models.CharField(
        'Фамилия', max_length=constants.MAX_NAME_LENGTH, blank=True
    )
    bio = models.TextField('Биография', blank=True)

    role = models.CharField(
        'Роль',
        max_length=max(len(role) for role, _ in UserRoles.choices),
        choices=UserRoles.choices,
        default=UserRoles.USER,
        help_text='Роль определяет права доступа'
    )

    confirmation_code = models.CharField(
    # Можно лучше: Можно не хранить код подтверждения в БД, если
    # использовать default_token_generator из django.contrib.auth.tokens.
    # У этого объекта есть два метода: для генерации токена - make_token
    # и для проверки полученного токена  - check_token (оба метода
    # принимают на вход объект пользователя).
        'Код подтверждения',
        max_length=6,
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
        """Проверяет, является ли пользователь администратором."""
        return self.role == (
            self.UserRoles.ADMIN
            or self.is_superuser
            or self.is_staff
        )

    @property
    def is_moderator(self):
        """Проверяет, является ли пользователь модератором."""
        return self.role == self.UserRoles.MODERATOR
