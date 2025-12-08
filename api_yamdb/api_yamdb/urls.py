from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    # TODO ВСЕ API под версией v1 (согласно документации)
    path('api/v1/', include('api.urls')),
    path('api/v1/', include('reviews.urls')),
    path(
        'redoc/',
        TemplateView.as_view(template_name='redoc.html'),
        name='redoc'
    ),
]
