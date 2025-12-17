from rest_framework import serializers
from django.conf import settings
from django.core.mail import send_mail
from content.models import Category, Genre, Title, Comment, Review
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from rest_framework import serializers
from django.shortcuts import get_object_or_404
from . import constants


User = get_user_model()


# Categories fields.


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор для категорий."""

    class Meta:
        model = Category
        fields = ('name', 'slug')


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор для жанров."""

    class Meta:
        model = Genre
        fields = ('name', 'slug')


class TitleReadSerializer(serializers.ModelSerializer):
    """Сериализатор для просмотра произведений."""
    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(many=True, read_only=True)
    rating = serializers.IntegerField(read_only=True, default=None)

    class Meta:
        model = Title
        fields = (
            'id', 'name', 'year', 'rating', 'description',
            'genre', 'category'
        )


class TitleWriteSerializer(serializers.ModelSerializer):
    """Сериализатор для добавления произведений."""
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all(),
        required=False,
        allow_null=True
    )
    genre = serializers.SlugRelatedField(
        slug_field='slug',
        many=True,
        queryset=Genre.objects.all(),
        allow_null=False,
        allow_empty=False,
    )

    class Meta:
        model = Title
        fields = (
            'id', 'name', 'year', 'description',
            'genre', 'category'
        )

    def to_representation(self, instance):
        return TitleReadSerializer(
            instance,
            context=self.context
        ).data


# Review fields.

class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор для отзывов."""
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
    )

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date')

    def validate(self, data):
        request = self.context['request']
        title_id = self.context['view'].kwargs.get('title_id')
        if request.method == 'POSt':
            if Review.objects.filter(
                title_id=title_id,
                author=request.user
            ).exists():
                raise serializers.ValidationError(
                    'Вы уже оставили отзыв на это произведение.'
                )
        return data


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор для комментариев."""
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
    )

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date')


# Users fields.

class UserSerializer(serializers.ModelSerializer):
    '''Сериализатор для модели User.'''

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name',
                  'last_name', 'bio', 'role')
        read_only_fields = ('email', 'username')


class UserMeSerializer(UserSerializer):
    '''Сериализатор для изменения профиля через /me/.'''

    class Meta(UserSerializer.Meta):
        read_only_fields = ('role',)


class UserSignUpSerializer(serializers.Serializer):
    '''Сериализатор для регистрации пользователя.'''
    email = serializers.EmailField(
        required=True,
        max_length=constants.MAX_EMAIL_LENGTH
    )
    username = serializers.CharField(
        required=True,
        max_length=constants.MAX_NAME_LENGTH,
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

    def create(self, validated_data):
        user, _ = User.objects.get_or_create(
            email=validated_data['email'],
            username=validated_data['username'],
            defaults={'is_active': True}
        )
        confirmation_code = default_token_generator.make_token(user)

        send_mail(
            subject='Код подтверждения YaMDb',
            message=f'Ваш код подтверждения: {confirmation_code}',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=False,
        )
        return user


class TokenObtainSerializer(serializers.Serializer):
    '''Сериализатор для получения JWT токена.'''
    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)

    def validate(self, data):
        username = data.get('username')
        confirmation_code = data.get('confirmation_code')

        user = get_object_or_404(User, username=username)

        if not default_token_generator.check_token(
            user, confirmation_code
        ):
            raise serializers.ValidationError(
                'Неверный код подтверждения'
            )

        data['user'] = user
        return data
