from rest_framework import permissions


class OwnerOrAdminPermissions(permissions.BasePermission):
    message = "You must be the owner of the object."

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return obj.f1Id == request.user or request.user.is_staff

class FriendOrAdminPermission(permissions.BasePermission):
    message = "You must be the owner of the object."

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return obj.f2Id == request.user or request.user.is_staff
