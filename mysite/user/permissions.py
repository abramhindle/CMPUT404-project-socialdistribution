from rest_framework import permissions


class OwnerPermissions(permissions.BasePermission):
    message = "You must be the owner of the object."

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return obj == request.user
