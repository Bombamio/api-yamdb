from django.core.validators import RegexValidator
from django.db import models
from django.contrib.auth.models import AbstractUser

MAX_USERNAME_LENGTH = 150
# TODO: Лучше создать отдельный файл для хранения константы в каждом
# приложении - constants.py
MAX_EMAIL_LENGTH = 254
MAX_NAME_LENGTH = 150
USERNAME_PATTERN = r'^[\w.@+-]+\Z'


class User(AbstractUser):
    '''Кастомизированная модель пользователя для YaMDb.'''
    # TODO: Тут и ниже:
    # В докстрингах всегда используются тройные двойные кавычки: """ ... """

    ROLE_USER = 'user'
    ROLE_MODERATOR = 'moderator'
    ROLE_ADMIN = 'admin'

    ROLE_CHOICES = [
    # Можно лучше: В Джанго есть подходящие енамы для организации вариантов выбора.
    # https://docs.djangoproject.com/en/3.2/ref/models/fields/#enumeration-types
        (ROLE_USER, 'Пользователь'),
        (ROLE_MODERATOR, 'Модератор'),
        (ROLE_ADMIN, 'Администратор'),
    ]

    username_validator = RegexValidator(
    # Можно лучше: Можно использовать данный атрибут из родительского
    # класса либо вынести валидатор из класса, чтобы можно было его
    # использовать еще и в сериализаторе для регистрации.
        regex=USERNAME_PATTERN,
        message='Имя пользователя может содержать только буквы, цифры'
    )

    username = models.CharField(
        'Имя пользователя',
        max_length=MAX_NAME_LENGTH,
        unique=True,
        validators=[username_validator],
        # TODO: Для поля username необходимы две проверки:
        # 1. На соответствие паттерну, указанному в спецификации
        # (ограничение допустимых символов)
        # 2. Запрет на использование me в качестве имени пользования.
        # Оба эти запрета стоит установить в параметре поля validators,
        # добавив туда соответствующие валидаторы. Тогда эти проверки
        # автоматически подтянутся модельными сериализаторами.
        # В части реализации валидации есть варианты:
        # 1. Для установления ограничения используемых символов можно
        # использовать встроенный валидатор - откройте исходники
        # AbstractUser - он в первой строке класса сразу после докстринга.
        # 2. В любом случае нам понадобится валидирующая функция,
        # которая запретит использование me. Но в ней можно еще
        # реализовать собственную улучшенную проверку использования
        # допустимых символов, которая будет сообщать пользователю какие
        # именно символы являются некорректными в введенным им варианте
        # имени пользователя (пригодится re.sub, которым можно убрать
        # все допустимые символы, оставив только недопустимые).
        help_text='Требуется. 150 символов или меньше. Только буквы, цифры'
    )

    email = models.EmailField(
        'Электронная почта',
        max_length=MAX_EMAIL_LENGTH,
        unique=True,
        help_text='Требуется. Уникальный email.'
    )

    first_name = models.CharField(
        'Имя', max_length=MAX_NAME_LENGTH, blank=True
    )
    last_name = models.CharField(
        'Фамилия', max_length=MAX_NAME_LENGTH, blank=True
    )
    bio = models.TextField('Биография', blank=True)

    role = models.CharField(
        'Роль',
        max_length=20,
        # TODO: Максимальную длину стоит задать с запасом, чтобы в
        # случае добавления новой роли мы не уперлись в лимит символов
        # (мы не знаем какую роль понадобится добавить).
        # Можно лучше:
        # Как вариант, можно прописать вычисление максимальной длины из
        # существующих ролей, т.е. взять длины всех ролей, и выбрать из
        # них максимальную. Это можно сделать прямо в этой строке.
        # Понадобится функция max, в которую надо передать список с
        # длинами ролей (его можно сформировать через list comprehension
        # или через функцию map и list.
        choices=ROLE_CHOICES,
        default=ROLE_USER,
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
    # Отлично: Хорошая идея.
        '''Проверяет, является ли пользователь администратором.'''
        return self.role == self.ROLE_ADMIN or self.is_superuser
        # TODO: Учтем тут, что стафф-пользователи (.is_staff) тоже имеют
        # доступ к админке и могут быть приравнены к админам.

    @property
    def is_moderator(self):
        '''Проверяет, является ли пользователь модератором.'''
        return self.role == self.ROLE_MODERATOR
