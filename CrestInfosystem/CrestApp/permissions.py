from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user and request.user.role == 'admin':
            return True
        if request.method in permissions.SAFE_METHODS:
            return True
        return False
