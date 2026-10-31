from rest_framework.permissions import BasePermission


class UserAccessPermission(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user and request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        user = request.user

        is_moderator = user.groups.filter(
            name='Модераторы'
        ).exists()

        return user.is_superuser or is_moderator or obj.pk == user.pk
