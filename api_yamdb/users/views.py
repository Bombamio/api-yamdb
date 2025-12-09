# api_yamdb/users/views.py
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken
from api.permissions import IsAdmin
from .serializers import (
    UserSerializer, UserCreateSerializer,
    UserSignUpSerializer, TokenObtainSerializer
)

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    '''ViewSet для управления пользователями.'''
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'
    permission_classes = [IsAdmin]

    def get_serializer_class(self):
        if self.action == 'create':
            return UserCreateSerializer
        return UserSerializer

    @action(
        detail=False,
        methods=['get', 'patch'],
        permission_classes=[permissions.IsAuthenticated]
    )
    def me(self, request):
        '''Эндпоинт для работы с собственным профилем (/api/v1/users/me/).'''
        if request.method == 'GET':
            serializer = self.get_serializer(request.user)
            return Response(serializer.data)

        elif request.method == 'PATCH':
            serializer = self.get_serializer(
                request.user,
                data=request.data,
                partial=True
            )
            serializer.is_valid(raise_exception=True)

            # Не позволяем менять роль через /me (по ТЗ)
            if 'role' in serializer.validated_data:
                serializer.validated_data.pop('role')

            serializer.save()
            return Response(serializer.data)


class SignUpView(APIView):
    '''Регистрация нового пользователя (/api/v1/auth/signup/).'''
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = UserSignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data
        email = data['email']
        username = data['username']

        # Проверяем, существует ли пользователь (мог быть создан админом)
        user, created = User.objects.get_or_create(
            email=email,
            username=username,
            defaults={'is_active': True}
        )

        # Генерируем confirmation_code
        # TODO: Потом реализуем отправку писем если нужно
        user.confirmation_code = '123456'  # Заглушка для тестов
        user.save()

        return Response({'email': email, 'username': username})


class TokenObtainView(APIView):
    '''Получение JWT токена (/api/v1/auth/token/).'''
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = TokenObtainSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data
        username = data['username']
        confirmation_code = data['confirmation_code']

        user = get_object_or_404(User, username=username)

        # Проверяем confirmation_code
        if user.confirmation_code != confirmation_code:
            return Response(
                {'error': 'Неверный код подтверждения'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Генерируем токен
        token = AccessToken.for_user(user)
        return Response({'token': str(token)})
