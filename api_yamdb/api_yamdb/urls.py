from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include([
        path('', include('api.urls')),       # ← api приложение
        path('', include('reviews.urls')),   # ← reviews приложение
        path('', include('users.urls')),      # ← users приложение
        #path('', include('categories.urls')),   # ← categories приложение
    ])),
    path(
        'redoc/',
        TemplateView.as_view(template_name='redoc.html'),
        name='redoc'
    ),
]
