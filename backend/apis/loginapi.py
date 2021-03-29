from ..models import Author
from ..serializers import AuthorSerializer


from django.contrib.auth import authenticate, login

from rest_framework.response import Response
from rest_framework import status, viewsets, permissions

import json


class LoginAPI(viewsets.ModelViewSet):

    queryset = Author.objects.all()

    permission_classes = [
        permissions.AllowAny
        #	permissions.IsAuthenticated
    ]

    lookup_field = 'id'

    serializer_class = AuthorSerializer

    def update(self, request, *args, **kwargs):

        queryset = Author.objects.all()

        body = json.loads(request.body)
        username = body['username']
        password = body['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            query_author = queryset.filter(user=user).get()
            serializer = self.get_serializer(query_author)

            return Response(serializer.data)

        else:
            print('Login error')
            return Response(status=status.HTTP_404_NOT_FOUND)
