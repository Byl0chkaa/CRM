from rest_framework.permissions import BasePermission

from apps.user.models import UserRole


class HasRole(BasePermission):
    allowed_roles = []

    def has_permission(self, request, view):
        return bool(
            request.user and request.user.is_authenticated
            and request.user.role in self.allowed_roles
        )


class IsAdminRole(HasRole):
    allowed_roles = [UserRole.ADMIN]


class IsManagerRole(HasRole):
    allowed_roles = [UserRole.MANAGER]


class IsOwnerOrAdminRole(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.role == UserRole.ADMIN:
            return True
        return obj.manager == request.user


class IsActiveUser(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user.is_authenticated and request.user.is_active
        )