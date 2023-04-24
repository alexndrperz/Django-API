from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

class IsAdmin(BaseAuthentication):
    def has_permission(self, request,view):
        user =request.user
        if user.groups.filter(name="administrator").exists() or user.is_superuser:
            return True
        else:
            return False

class IsAdmin(BaseAuthentication):
    def has_permission(self, request,view):
        user =request.user
        if user.groups.filter(name="administrator").exists() or user.is_superuser:
            return True
        else:
            return False

        