from django.core.exceptions import ValidationError


def validate_username(value):
    '''Запрещает имя пользователя "me".'''
    if value and value.lower() == 'me':
        raise ValidationError(
            'Имя пользователя "me" не разрешено'
        )
    return value
