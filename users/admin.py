from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


# Константы для админки
PERSONAL_FIELDS = ('username', 'email', 'first_name', 'last_name')


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    '''Админка для кастомной модели User.'''

    list_display = PERSONAL_FIELDS + ('role', 'is_active')
    list_filter = ('role', 'is_active', 'is_staff', 'is_superuser')
    search_fields = PERSONAL_FIELDS

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Персональная информация', {
            'fields': ('first_name', 'last_name', 'email', 'bio')
        }),
        ('Права доступа', {
            'fields': (
                'role', 'is_active', 'is_staff', 'is_superuser',
                'groups', 'user_permissions'
            )
        }),
        ('Важные даты', {'fields': ('last_login', 'date_joined')}),
        ('Подтверждение', {'fields': ('confirmation_code',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': PERSONAL_FIELDS + ('password1', 'password2', 'role'),
        }),
    )
