from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ReviewViewSet, CommentViewSet

router = DefaultRouter()

# Эндпоинты для отзывов
router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='reviews'
)

# Эндпоинты для комментариев
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments'
)

urlpatterns = [
    path('', include(router.urls)),
]
