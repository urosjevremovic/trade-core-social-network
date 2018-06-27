from rest_framework import permissions


class IsAnonymousUser(permissions.BasePermission):
    message = 'You can not register new account while you are logged in'

    def has_permission(self, request, view):
            return request.user.is_anonymous


class IsAccountwnerOrAdminUserOrReadOnly(permissions.BasePermission):
    message = 'You are not the owner of this post.'

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            return obj == request.user or request.user.is_staff