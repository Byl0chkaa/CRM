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

class IsAdminOrManagerRole(HasRole):
    allowed_roles = [UserRole.ADMIN, UserRole.MANAGER]



class IsActiveUser(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user.is_authenticated and request.user.is_active
        )

class IsAssignmentManager(BasePermission):
    def has_object_permission(self, request, view, obj):
        if obj.manager is None:
            return True
        return obj.manager == request.user