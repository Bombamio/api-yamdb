from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator
from rest_framework import serializers

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    '''Сериализатор для модели User.'''

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name',
                  'last_name', 'bio', 'role')
        read_only_fields = ('email', 'username')
        extra_kwargs = {
            'role': {'required': False},
            'first_name': {'max_length': 150},
            'last_name': {'max_length': 150},
            'bio': {'allow_blank': True},
        }


class UserMeSerializer(serializers.ModelSerializer):
    '''Сериализатор для изменения профиля через /me/.'''

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'bio')
        extra_kwargs = {
            'username': {
                'max_length': 150,
                'validators': [RegexValidator(
                    regex=r'^[\w.@+-]+\Z',
                    message='Имя пользователя может содержать только буквы, цифры и @/./+/-/_'
                )]
            },
            'email': {'max_length': 254},
            'first_name': {'max_length': 150},
            'last_name': {'max_length': 150},
            'bio': {'allow_blank': True},
        }

    def validate_username(self, value):
        '''Запрещает имя пользователя "me".'''
        if value and value.lower() == 'me':
            raise serializers.ValidationError(
                'Имя пользователя "me" не разрешено'
            )
        return value

    def validate(self, data):
        '''Проверяет уникальность email и username.'''
        user = self.instance
        email = data.get('email')
        username = data.get('username')

        if email and email != user.email:
            if User.objects.filter(email=email).exclude(id=user.id).exists():
                raise serializers.ValidationError({
                    'email': 'Этот email уже используется другим пользователем.'
                })

        if username and username != user.username:
            if User.objects.filter(username=username).exclude(id=user.id).exists():
                raise serializers.ValidationError({
                    'username': 'Этот username уже используется другим пользователем.'
                })

        return data


class UserCreateSerializer(serializers.ModelSerializer):
    '''Сериализатор для создания пользователя администратором.'''

    class Meta:
        model = User
        fields = ('username', 'email', 'role',
                  'first_name', 'last_name', 'bio')
        extra_kwargs = {
            'first_name': {'max_length': 150, 'required': False},
            'last_name': {'max_length': 150, 'required': False},
            'bio': {'required': False, 'allow_blank': True},
        }

    def create(self, validated_data):
        '''Создает пользователя с неиспользуемым паролем.'''
        user = User.objects.create(**validated_data)
        user.set_unusable_password()
        user.save()
        return user


class UserSignUpSerializer(serializers.Serializer):
    '''Сериализатор для регистрации пользователя.'''
    email = serializers.EmailField(required=True, max_length=254)
    username = serializers.CharField(
        required=True,
        max_length=150,
        validators=[RegexValidator(
            regex=r'^[\w.@+-]+\Z',
            message='Имя пользователя может содержать только буквы, цифры и @/./+/-/_'
        )]
    )

    def validate_username(self, value):
        '''Запрещает имя пользователя "me".'''
        if value.lower() == 'me':
            raise serializers.ValidationError(
                'Имя пользователя "me" не разрешено'
            )
        return value

    def validate(self, data):
        '''Проверяет уникальность email и username.'''
        email = data.get('email')
        username = data.get('username')

        email_user = User.objects.filter(email=email).first()
        username_user = User.objects.filter(username=username).first()

        if email_user and username_user and email_user != username_user:
            raise serializers.ValidationError(
                'Пользователь с таким email или username уже существует'
            )
        elif email_user and email_user.username != username:
            raise serializers.ValidationError(
                'Пользователь с таким email уже существует'
            )
        elif username_user and username_user.email != email:
            raise serializers.ValidationError(
                'Пользователь с таким username уже существует'
            )

        return data


class TokenObtainSerializer(serializers.Serializer):
    '''Сериализатор для получения JWT токена.'''
    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)
