import requests
import base64
from rest_framework import permissions
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
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


def IsLocalAuthor(request):
    try:
        request_uri = request.META['HTTP_REFERER']
        # token_auth_value = token_auth.split('Token ')[1]
        if (DJANGO_DEFAULT_HOST.split('/api/')[0] in request_uri or "http://localhost:3000/" in request_uri):
            return True
        else:
            return False
    except:
        return False

class IsAuthenticated(permissions.BasePermission):
    """
    Object-level permission to allow an authenticated node to access or edit objects
    """
    def has_permission(self, request, view):
        try:
            request_uri = request.META['HTTP_REFERER']
            if (DJANGO_DEFAULT_HOST.split('/api/')[0].split("//")[1] in request_uri or "localhost" in request_uri):
                if (("PostDetail" not in str(view) ) or (request.method in permissions.SAFE_METHODS)):
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
        except:
            #do nothing
            pass
        try:
            # https://stackoverflow.com/questions/10613315/accessing-request-headers-on-django-python
            basic_auth_field = request.META['HTTP_AUTHORIZATION']
            basic_auth_base64 = basic_auth_field.split("Basic ")[1]
            basic_auth_bytes = base64.b64decode(basic_auth_base64) 
            basic_auth_value = basic_auth_bytes.decode('utf-8')
            # Get the node from the request(will fail if node is not in our database)
            node = Node.objects.get(auth_info=basic_auth_value)
        except:
            return False
        return True

    #def is_author_or_read_only(self, request, view):
    #    if (("PostDetail" not in str(view) ) or (request.method in permissions.SAFE_METHODS)):
    #        return True
    #    try:
            # Get the user from the request
    #        author_id = request.user.author.id
    #        uri = request.build_absolute_uri()
    #    except:
    #        return False
    #    uuid_pattern_1 = "[A-Za-z0-9]{8}-[A-Za-z0-9]{4}-[A-Za-z0-9]{4}-[A-Za-z0-9]{4}-[A-Za-z0-9]{12}"
    #    uuid_pattern_2 = "[A-Za-z0-9]{36}"
    #    uuid_1 = re.findall(uuid_pattern_1, uri)
    #    uuid_2 = re.findall(uuid_pattern_2, uri)
    #    if len(uuid_1) != 0:
    #        return uuid_1[0] == str(author_id)
    #    elif len(uuid_2) != 0:
    #        return uuid_2[0] == str(author_id)
    #    return False