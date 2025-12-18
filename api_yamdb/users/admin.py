from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


User = get_user_model()


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Кастомная админка для модели User."""

    # Поля для списка пользователей
    list_display = ('username', 'email', 'first_name',
                    'last_name', 'role', 'is_staff')
    list_filter = ('role', 'is_staff', 'is_superuser', 'is_active')
    search_fields = ('username', 'email', 'first_name', 'last_name')

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {
         'fields': ('first_name', 'last_name', 'email', 'bio')}),
        ('Permissions', {
            'fields': ('role', 'is_active', 'is_staff', 'is_superuser',
                       'groups', 'user_permissions'),
        }),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'role'),
        }),
    )

    ordering = ('username',)
    filter_horizontal = ('groups', 'user_permissions',)
