
from rest_framework.permissions import BasePermission, SAFE_METHODS


MODERATOR_GROUP = 'Модераторы'


def is_moderator(user):
    return (
        user.is_authenticated
        and user.groups.filter(name=MODERATOR_GROUP).exists()
    )


class MaterialPermission(BasePermission):
    """
    Обычный пользователь работает только со своими материалами.
    Модератор может читать и редактировать любые материалы,
    но не может создавать или удалять их.
    """

    def has_permission(self, request, view):
        user = request.user

        if not user or not user.is_authenticated:
            return False

        action = getattr(view, 'action', None)

        # Для ViewSet проверяем действие напрямую.
        if action in ('create', 'destroy'):
            return not is_moderator(user)

        # Для GenericAPIView проверяем HTTP-метод.
        if request.method in ('POST', 'DELETE'):
            return not is_moderator(user)

        return True

    def has_object_permission(self, request, view, obj):
        user = request.user

        if is_moderator(user):
            # Модератору запрещены POST/DELETE выше,
            # но читать и редактировать чужие объекты можно.
            return request.method not in ('POST', 'DELETE')

        return obj.owner_id == user.id
