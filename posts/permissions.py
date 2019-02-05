from rest_framework import permissions


class IsSelf(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method == 'post':
            return request.user.is_anonymous
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj == request.user
