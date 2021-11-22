from rest_framework import permissions
from rest_framework.authtoken.models import Token

from .models import Author, Node
import re

from social_dist.settings import DJANGO_DEFAULT_HOST 

class IsAuthorOrReadOnly(permissions.BasePermission):
    """
    Object-level permission to allow the author of the object to edit it.
    """
    message = "Author is not allowed to do this operation"
    
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        try:
            # Get the user from the request
            author_id = request.user.author.id
            uri = request.build_absolute_uri()
        except:
            return False
        uuid_pattern_1 = "[A-Za-z0-9]{8}-[A-Za-z0-9]{4}-[A-Za-z0-9]{4}-[A-Za-z0-9]{4}-[A-Za-z0-9]{12}"
        uuid_pattern_2 = "[A-Za-z0-9]{36}"
        uuid_1 = re.findall(uuid_pattern_1, uri)
        uuid_2 = re.findall(uuid_pattern_2, uri)
        if len(uuid_1) != 0:
            return uuid_1[0] == str(author_id)
        elif len(uuid_2) != 0:
            return uuid_2[0] == str(author_id)
        return False
        # Match the author ID to the URL of the request

class IsAuthenticatedNode(permissions.BasePermission):
    """
    Object-level permission to allow an authenticated node to acess or edit objects
    """
    basic_auth = "YWxhZGRpbjpvcGVuc2VzYW1r"
    def has_permission(self, request, view):
        try:
            #request_uri2 = request.get_host()
            #request_uri3 = request.META['REMOTE_HOST']
            request_uri = request.META['HTTP_REFERER']
            print(request_uri)
            if (request_uri in DJANGO_DEFAULT_HOST):
                return True #request is not from a foreign node
            # Get the node from the request(will fail if node is not in our database)
            node = Node.objects.get(host=request_uri)
            # https://stackoverflow.com/questions/10613315/accessing-request-headers-on-django-python
            basic_auth_field = request.META['HTTP_AUTHORIZATION']
            basic_auth_value = basic_auth_field.split("Token ")[1]
            if (basic_auth_value != basic_auth):
                return False
        except:
            return False
        return True

