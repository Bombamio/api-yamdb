import random

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404

from rest_framework import filters, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken

from api.permissions import IsAdmin
from .serializers import (
    TokenObtainSerializer,
    UserCreateSerializer,
    UserMeSerializer,
    UserSerializer,
    UserSignUpSerializer,
)

User = get_user_model()


def generate_confirmation_code():
    '''Генерирует 6-значный код подтверждения.'''
    return ''.join(str(random.randint(0, 9)) for _ in range(6))


class CustomPagination(PageNumberPagination):
    '''Кастомная пагинация.'''
    page_size = 10
    page_size_query_param = 'limit'
    max_page_size = 100


class UserViewSet(viewsets.ModelViewSet):
    '''ViewSet для управления пользователями администратором.'''
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'
    permission_classes = [IsAdmin]
    pagination_class = CustomPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['username', 'email']
    http_method_names = ['get', 'post', 'patch', 'delete', 'head', 'options']

    def get_serializer_class(self):
        '''Возвращает сериализатор для действия.'''
        if self.action == 'create':
            return UserCreateSerializer
        return UserSerializer

    def create(self, request, *args, **kwargs):
        '''Создание пользователя администратором.'''
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        # Генерируем код подтверждения
        user.confirmation_code = generate_confirmation_code()
        user.save()

        response_serializer = UserSerializer(user)
        headers = self.get_success_headers(serializer.data)
        return Response(
            response_serializer.data,
            status=status.HTTP_201_CREATED,
            headers=headers
        )

    @action(
        detail=False,
        methods=['get', 'patch'],
        permission_classes=[permissions.IsAuthenticated]
    )
    def me(self, request):
        '''Эндпоинт для работы с собственным профилем.'''
        if request.method == 'GET':
            serializer = self.get_serializer(request.user)
            return Response(serializer.data)

        elif request.method == 'PATCH':
            serializer = UserMeSerializer(
                request.user,
                data=request.data,
                partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)


class SignUpView(APIView):
    '''Регистрация пользователя с отправкой кода подтверждения.'''
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        '''Обработка POST-запроса.'''
        serializer = UserSignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data
        email = data['email']
        username = data['username']

        user, created = User.objects.get_or_create(
            email=email,
            username=username,
            defaults={'is_active': True}
        )

        user.confirmation_code = generate_confirmation_code()
        user.save()

        send_mail(
            subject='Код подтверждения YaMDb',
            message=f'Ваш код подтверждения: {user.confirmation_code}',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
            fail_silently=False,
        )

        return Response(
            {'email': email, 'username': username},
            status=status.HTTP_200_OK
        )


class TokenObtainView(APIView):
    '''Получение JWT токена по коду подтверждения.'''
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        '''Обработка POST-запроса.'''
        serializer = TokenObtainSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data
        username = data['username']
        confirmation_code = data['confirmation_code']

        user = get_object_or_404(User, username=username)

        if user.confirmation_code != confirmation_code:
            return Response(
                {'error': 'Неверный код подтверждения'},
                status=status.HTTP_400_BAD_REQUEST
            )

        token = AccessToken.for_user(user)
        return Response({'token': str(token)})
