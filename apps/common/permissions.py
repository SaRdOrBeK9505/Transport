from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdminOrReadOnly(BasePermission):
    """
    GET, HEAD, OPTIONS — hamma uchun (public frontend).
    POST, PUT, PATCH, DELETE — faqat is_staff (admin/superuser).
    """
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_authenticated and request.user.is_staff)


class IsAdminUser(BasePermission):
    """Faqat is_staff=True bo'lgan foydalanuvchilar."""
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.is_staff)


class IsDispatcherOrAdmin(BasePermission):
    """Admin yoki dispatcher roli bo'lgan autentifikatsiyalangan foydalanuvchi."""
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        return (
            request.user.is_staff or
            getattr(request.user, 'role', None) in ('admin', 'dispatcher')
        )
