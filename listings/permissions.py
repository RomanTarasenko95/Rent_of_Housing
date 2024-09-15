from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsOwnerOrReadOnly(BasePermission):
    """
    Разрешает доступ только владельцу объекта для изменения, остальным - только чтение.
    """

    def has_object_permission(self, request, view, obj):
        # Доступ разрешен только для безопасных методов (GET, HEAD, OPTIONS)
        if request.method in SAFE_METHODS:
            return True

        # Проверка, является ли пользователь владельцем объявления (owner)
        if hasattr(obj, 'owner'):
            return obj.owner == request.user

        # Если объект не имеет атрибута 'owner', доступ запрещен
        return False


class IsAuthenticatedOrReadOnly(BasePermission):
    """
    Разрешает доступ аутентифицированным пользователям или только чтение.
    """

    def has_permission(self, request, view):
        # Разрешить безопасные методы (GET, HEAD, OPTIONS) всем
        if request.method in SAFE_METHODS:
            return True

        # Только аутентифицированные пользователи могут использовать небезопасные методы (POST, PUT, DELETE)
        return request.user.is_authenticated


class IsRenterOrReadOnly(BasePermission):
    """
    Разрешает просмотр и фильтрацию для арендаторов (всех аутентифицированных пользователей).
    """

    def has_permission(self, request, view):
        # Все пользователи могут просматривать и фильтровать объявления
        return request.method in SAFE_METHODS or request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Доступ разрешен только для безопасных методов (GET, HEAD, OPTIONS)
        if request.method in SAFE_METHODS:
            return True
        return False  # Только арендаторы могут просматривать и фильтровать
