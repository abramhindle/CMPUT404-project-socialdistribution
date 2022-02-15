from django.shortcuts import render
from django.core.exceptions import ValidationError
from django.core.validators import URLValidator
from rest_framework import status
from rest_framework import viewsets
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import api_view, renderer_classes
import requests as r
from .models import Post
from authors.models import Author
from .serializers import PostReadSerializer, PostWriteSerializer

class CustomPageNumberPagination(PageNumberPagination):
    page_size_query_param = 'size'

    def get_paginated_response(self, data):
        return Response({'type': "posts", 'items': data})

class PostViewSet(viewsets.ModelViewSet):
    authentication_classes = []
    pagination_class = CustomPageNumberPagination

    def get_serializer_class(self):
        method = self.request.method
        if method == 'PUT' or method == 'POST':
            return PostWriteSerializer
        else:
            return PostReadSerializer

    def get_queryset(self):
        author_id = self.kwargs.get('author_id')
        posts = Post.objects.filter(author=author_id)
        return posts

@api_view(['GET'])
@renderer_classes([JSONRenderer])
def get_post(request, path):
    try:  # If Path Is A URL, We Need To Make A Request To Another Server
        validate = URLValidator()
        validate(path)
        response = r.get(path)
        return Response(response.json(), status=status.HTTP_200_OK if response.status_code == 200 else status.HTTP_404_NOT_FOUND)
    except ValidationError:  # If Path Is Not A URL, We Make The Request To Our Own Server
        return PostViewSet.as_view(actions={"get": "retrieve"})(request._request, pk=path)

@api_view(['GET'])
@renderer_classes([JSONRenderer])
def get_posts(request):
    return PostViewSet.as_view(actions={"get": "list"})(request._request)