from rest_framework.permissions import BasePermission

from .exceptions import IsAuthenticated, IsNotAuthenticated, PermissionDenied

class CustomIsAuthenticated(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            raise IsNotAuthenticated()
        return True

class CustomIsNotAuthenticated(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            raise IsAuthenticated()
        return True
