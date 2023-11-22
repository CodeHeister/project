from rest_framework.permissions import BasePermission

from .exceptions import Authenticated, NotAuthenticated, PermissionDenied

class CustomIsAuthenticated(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            raise NotAuthenticated()
        return True

class CustomNotAuthenticated(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            raise Authenticated()
        return True
