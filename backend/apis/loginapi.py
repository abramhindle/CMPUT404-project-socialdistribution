from ..models import Author
from ..serializers import AuthorSerializer


from django.contrib.auth import authenticate, login

from rest_framework.response import Response
from rest_framework import status, viewsets, permissions

import json


class LoginAPI(viewsets.ModelViewSet):
    """
    This class handles requests for login by a user of the webserver. By taking in a username and password then authenticating the user.
    """
    permission_classes = [
        permissions.AllowAny
    ]

    lookup_field = 'id'
    # Set the serializer
    serializer_class = AuthorSerializer

    def update(self, request, *args, **kwargs):
        """
        This method will take a username and password in the request body, and responding wiht a valid Author if the request is authenticated.
        """
        # Load the request into a json
        body = json.loads(request.body)
        # Authenticate the requested username and password
        user = authenticate(
            request, username=body['username'], password=body['password'])
        # If a user is returned perform a validated login session, return the author object for the user
        if user is not None:
            login(request, user)
            return Response(self.get_serializer(Author.objects.filter(user=user).get()).data, status=status.HTTP_200_OK)
        # Else return a 403 Forbidden as the user is not authenticated
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)
