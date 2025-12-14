from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, SignUpView, TokenObtainView

router = DefaultRouter()
router.register('users', UserViewSet, basename='users')

urlpatterns = [
    # Эти пути будут: /api/v1/auth/signup/ и /api/v1/auth/token/
    path('auth/signup/', SignUpView.as_view(), name='signup'),
    path('auth/token/', TokenObtainView.as_view(), name='token'),
    
    # А это будет: /api/v1/users/ (через router)
    path('', include(router.urls)),
]