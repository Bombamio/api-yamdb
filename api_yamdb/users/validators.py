from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.exceptions import ValidationError


def validate_username(value):
    """Запрещает имя пользователя "me"."""
    if value and value.lower() == 'me':
        raise ValidationError(
            'Имя пользователя "me" не разрешено'
        )
    return value


username_validator = UnicodeUsernameValidator(
    message=(
        'Имя пользователя может содержать только буквы, цифры и '
        '@/./+/-/_'
    )
)
