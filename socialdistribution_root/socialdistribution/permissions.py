# DRF permissions: https://www.django-rest-framework.org/tutorial/4-authentication-and-permissions/

from rest_framework.permissions import BasePermission, SAFE_METHODS
from re import search

class IsOwnerOrReadOnly(BasePermission):
    # Validates access to resource by the requester or READ only
    def has_permission(self, request, view):
        # Read permissions are allowed to any request
        if request.method in SAFE_METHODS:
            return True

        # Reject if not authenticated
        if not (bool(request.user and request.user.is_authenticated)):
            return False

        # Checking user performing requests on own resource
        # NOTE: might need to be adjusted for other API calls?
        res = search('author/(.*?)/', request.path)
        if res:
            author_id = res.group(1)
            return author_id == str(request.user.id)

        # Unhandled resource path
        return False

    # Validates requester is an owner of the object accessing
    # theoretically, the has_permissions validates it already, but could be useful for fine-grained access
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request
        if request.method in SAFE_METHODS:
            return True

        # NOTE:
        # I am assuming owners of all our objects will be author as in case with posts/comments
        # if it is otherwise, will need to make separate permissions
        try:
            return obj.author == request.user
        except AttributeError: 
            return False