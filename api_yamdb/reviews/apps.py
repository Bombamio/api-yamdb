from django.apps import AppConfig


class ReviewsConfig(AppConfig):
    '''
    Конфигурация приложения Reviews для управления отзывами и комментариями.
    '''
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'reviews'
    verbose_name = 'Отзывы и комментарии'
