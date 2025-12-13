from django.urls import include, path

urlpatterns = [
    path('', include('users.urls')),  # Все users.urls в корне api/v1/
    path('', include('categories.urls')),
    path('', include('reviews.urls')),
]