from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsOwnerOrReadOnly(BasePermission):
    """
    Разрешает доступ только владельцу объекта для изменения, остальным - только чтение.
    """
    def has_object_permission(self, request, view, obj):
        # Доступ разрешен только для безопасных методов (GET, HEAD, OPTIONS)
        if request.method in SAFE_METHODS:
            return True
        # Проверка, является ли пользователь владельцем объекта
        return obj.owner == request.user


class IsRenterOrReadOnly(BasePermission):
    """
    Разрешает просмотр и фильтрацию для арендаторов.
    """
    def has_permission(self, request, view):
        # Все пользователи могут просматривать и фильтровать объявления
        return request.method in SAFE_METHODS or request.user.is_authenticated
