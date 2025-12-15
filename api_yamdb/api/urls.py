from django.urls import include, path

# TODO: Лишняя пустая строка.
from rest_framework.routers import DefaultRouter

from users.views import SignUpView, TokenObtainView, UserViewSet

from .views import (
    CategoryViewSet,
    CommentViewSet,
    GenreViewSet,
    ReviewViewSet,
    TitleViewSet,
)


router = DefaultRouter()
# TODO: Тут лучше дать роутеру имя, содержащее номер версии API. Так
# меньше шансев запутаться при появлении новых версий.
# Обычно используют префикс с номером версии (т.е. в начале имени
# указывают версию).

# Categories fields.
router.register(r'categories', CategoryViewSet, basename='categories')
# TODO: r-строки нужны только если в урле есть регулярное выражение. Убери лишние r
router.register(r'genres', GenreViewSet, basename='genres')
router.register(r'titles', TitleViewSet, basename='titles')

# Review fields.
router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='reviews'
)
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments'
)

# Users fields.
router.register('users', UserViewSet, basename='users')


urlpatterns = [
    path('auth/signup/', SignUpView.as_view(), name='signup'),
    path('auth/token/', TokenObtainView.as_view(), name='token'),
    path('', include(router.urls)),
]
