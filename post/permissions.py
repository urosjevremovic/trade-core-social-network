from rest_framework import permissions


class IsPostOwnerOrAdminUserOrReadOnly(permissions.BasePermission):
    message = 'You are not the owner of this post.'

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            return obj.author == request.user or request.user.is_staff