from django.apps import AppConfig


class CategoriesConfig(AppConfig):
    '''Конфигурация приложения Categories.'''
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'categories'
    verbose_name = 'Категории и произведения'
