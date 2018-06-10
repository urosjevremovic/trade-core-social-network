from rest_framework.permissions import BasePermission


class IsPostOwnerOrReadOnly(BasePermission):
    message = 'You are not the owner of this post.'

    def has_object_permission(self, request, view, obj):
        return obj.author == request.user


class IsAccountOwnerOrReadOnly(BasePermission):
    message = 'You are not the owner of this account.'

    def has_object_permission(self, request, view, obj):
        return obj.pk == request.user.pk or request.user.is_staff


class IsAnonymousUser(BasePermission):
    message = 'You can not register new account while you are logged in'

    def has_permission(self, request, view):
        return request.user.is_anonymous