from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

class IsAdmin(BaseAuthentication):
    def has_permission(self, request,view):
        user =request.user
        if user.groups.filter(name="administrator").exists() or user.is_superuser:
            return True
        else:
            return False

class IsSeller(BaseAuthentication):
    def has_permission(self, request,view):
        user =request.user
        if user.groups.filter(name="sellers").exists():
            return True
        else:
            return False
    
    def has_object_permission(self, request, view, obj):
        if request.user.id == obj.seller_id or request.user.is_superuser==True:
            return True
        else:
            return False
        return True


class IsBuyer(BaseAuthentication):
    def has_permission(self, request,view):
        user =request.user
        if user.groups.filter(name="buyers").exists() or is_superuser:
            return True
        else:
            return False

    def has_object_permission(self, request, view, obj):
        if request.user.id == obj.buyers_id or request.user.is_superuser==True:
            return True
        else:
            return False
        return True

class IsChecker(BaseAuthentication):
    def has_permission(self, request,view):
        user =request.user
        if user.groups.filter(name="checkers").exists():
            return True
        else:
            return False

class IsGroupAccepted(BaseAuthentication):
    def has_permission(self, request, view):
        user =request.user
        isChecker = user.groups.filter(name="checkers").exists()
        isBuyer = user.groups.filter(name="buyers").exists()
        isSeller = user.groups.filter(name="sellers").exists()
        isAdmin = user.groups.filter(name="administrator").exists()

        if isChecker or isBuyer or IsSeller or isAdmin or user.is_superuser:
            return True
        else:
            return False

    def has_object_permission(self, request, view, obj):
        return True

        