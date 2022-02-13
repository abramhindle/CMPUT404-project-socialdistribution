from rest_framework import status
from rest_framework.decorators import action
from urllib.parse import urlparse
from django.conf import settings
from django.db.utils import IntegrityError
from django.core.exceptions import ValidationError
from .models import Author
from django.core.validators import URLValidator
from django.contrib.auth.models import User
from .serializers import AuthorSerializer
from rest_framework import viewsets
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from django.shortcuts import get_object_or_404
import requests as r
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.pagination import PageNumberPagination


class CustomPageNumberPagination(PageNumberPagination):
    page_size_query_param = 'size'

    def get_paginated_response(self, data):
        return Response({'type': "authors", 'items': data})


class AuthorViewSet(viewsets.ModelViewSet):
    authentication_classes = []
    serializer_class = AuthorSerializer
    queryset = Author.objects.all()
    pagination_class = CustomPageNumberPagination

    @action(detail=False, methods=['post'])
    def register(self, request):
        try:
            user = User.objects.create_user(username=request.data["displayName"], password=request.data["password"])
            author = user.author
            author.github = "https://www.github.com/" + request.data["github"]
            author.save()
            return Response(AuthorSerializer(author).data)
        except IntegrityError:
            return Response({"error": "Username Already Exists!"}, status=status.HTTP_409_CONFLICT)


@api_view(['GET'])
@renderer_classes([JSONRenderer])
def get_author(request, path):
    try:  # If Path Is A URL, We Need To Make A Request To Another Server
        validate = URLValidator()
        validate(path)
        response = r.get(path)
        return Response(response.json(), status=status.HTTP_200_OK if response.status_code == 200 else status.HTTP_404_NOT_FOUND)
    except ValidationError:  # If Path Is Not A URL, We Make The Request To Our Own Server
        return AuthorViewSet.as_view(actions={"get": "retrieve"})(request._request, pk=path)


@api_view(['GET'])
@renderer_classes([JSONRenderer])
def get_authors(request):
    return AuthorViewSet.as_view(actions={"get": "list"})(request._request)
