from rest_framework import permissions
from django.contrib.auth.models import User
from authors.models import Author


class IsOwnerOrAdmin(permissions.BasePermission):
    """Only Allow Owners Or Admins To Access The Object"""

    @staticmethod
    def get_owner(obj):
        raise NotImplementedError

    def has_permission(self, request, view):
        author: Author = view.kwargs["author"]
        current_user: User = request.user
        return current_user.author.local_id == author or current_user.is_staff

    def has_object_permission(self, request, view, obj):
        current_user: User = request.user
        owner = self.get_owner(obj)
        return owner.pk == current_user.pk or current_user.is_staff
