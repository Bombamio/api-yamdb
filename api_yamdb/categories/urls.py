from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()

# Эндпоинты для тайтлов.
router.register(
    'title',
    views.TitleViewSet,
    basename='title'
)

urlpatterns = [
    path('', include(router.urls)),
    path(
        'categories/',
        views.CategoryListCreateView.as_view(),
        name='list_create_categories'
    ),
    path(
        'categories/<slug:slug>/',
        views.CategoryDestroyView.as_view(),
        name='delete_categories'
    ),
    path(
        'genres/',
        views.GenreListCreateView.as_view(),
        name='list_create_genres'
    ),
    path(
        'genres/<slug:slug>/',
        views.GenreDestroyView.as_view(),
        name='delete_genres'
    ),
]
