from rest_framework import permissions


class IsAuthorOrModeratorOrAdminOrReadOnly(permissions.BasePermission):
    """
    Общее ограничение доступа с возможностью редактирования только
    автором, модератором или админом.
    """

    def has_object_permission(self, request, view, obj):
        return (
            request.method in (permissions.SAFE_METHODS) or
            obj.author == request.user or
            request.user.is_moderator or
            request.user.is_admin
        )


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Ограничение, позволяющее редактировать группы, категории
    и произведения только админом или суперюзером.
    """

    def has_permission(self, request, view):
        return (
            request.method in (permissions.SAFE_METHODS) or
            request.user.is_authenticated
            and request.user.is_admin
        )
