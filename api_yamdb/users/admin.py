from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
# TODO: Это не универсальный переводчик. Умеет переводить только заранее
# заготовленные фразы.
# Его можно расширить, обогатив своими фразами, но мы не будем заниматься
# этим в рамках проекта.
# Уберем

from .models import User
# TODO: Модель пользователей получаем через функцию get_user_model

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    '''Кастомная админка для модели User.'''
    # TODO: Тут и ниже:
    # В докстрингах всегда используются тройные двойные кавычки: """ ... """

    # Поля для списка пользователей
    list_display = ('username', 'email', 'first_name',
                    'last_name', 'role', 'is_staff')
    list_filter = ('role', 'is_staff', 'is_superuser', 'is_active')
    search_fields = ('username', 'email', 'first_name', 'last_name')

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {
         'fields': ('first_name', 'last_name', 'email', 'bio')}),
        (_('Permissions'), {
            'fields': ('role', 'is_active', 'is_staff', 'is_superuser',
                       'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'role'),
        }),
    )

    ordering = ('username',)
    filter_horizontal = ('groups', 'user_permissions',)
