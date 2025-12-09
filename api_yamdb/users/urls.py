from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, SignUpView, TokenObtainView

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='users')

urlpatterns = [
    path('', include(router.urls)),
    path('auth/signup/', SignUpView.as_view(), name='signup'),
    path('auth/token/', TokenObtainView.as_view(), name='token'),
]
