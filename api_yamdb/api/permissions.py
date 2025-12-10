from rest_framework import permissions


class IsAdmin(permissions.BasePermission):
    '''Разрешение только для администраторов.'''

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.is_admin
        )


# TODO: Для: Объектов без автора (категории, жанры, пользователи)
class IsAdminOrReadOnly(permissions.BasePermission):
    '''
    Разрешение на изменение только для администраторов.
    Чтение разрешено всем.
    '''

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or (request.user.is_authenticated and request.user.is_admin)
        )