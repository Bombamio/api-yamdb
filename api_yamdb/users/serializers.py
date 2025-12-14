from django.contrib.auth import get_user_model
from django.conf import settings
from rest_framework import serializers
from django.core.validators import RegexValidator

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    '''Сериализатор для модели User.'''
    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name',
            'last_name', 'bio', 'role'
        )
        extra_kwargs = {
            'role': {'required': False}
        }


class UserCreateSerializer(serializers.ModelSerializer):
    '''Сериализатор для создания пользователя администратором.'''
    class Meta:
        model = User
        fields = ('username', 'email', 'role')

    def create(self, validated_data):
        # Создаем пользователя без пароля (пароль установится позже)
        user = User.objects.create(**validated_data)
        user.set_unusable_password()  # Пароль будет установлен через email
        user.save()
        return user


class UserSignUpSerializer(serializers.Serializer):
    '''Сериализатор для регистрации пользователя.'''
    email = serializers.EmailField(required=True, max_length=150)
    username = serializers.CharField(
        required=True,
        max_length=settings.MAX_LENGTH_NAME,
        validators=[RegexValidator(
            regex=r'^[\w.@+-]+\Z',
            message=('Имя пользователя может содержать только буквы, '
                     'цифры и @/./+/-/_')
        )]
    )

    def validate_username(self, value):
        if value.lower() == 'me':
            raise serializers.ValidationError(
                'Имя пользователя "me" не разрешено'
            )
        return value

    def validate(self, data):
        # Проверяем, что пользователь с таким email или username уже существует
        email = data.get('email')
        username = data.get('username')

        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError(
                'Пользователь с таким email уже существует'
            )
        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError(
                'Пользователь с таким username уже существует'
            )
        return data


class TokenObtainSerializer(serializers.Serializer):
    '''Сериализатор для получения токена.'''
    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)
