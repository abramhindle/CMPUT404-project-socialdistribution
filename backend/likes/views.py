
from urllib import response
from django.http import Http404
from rest_framework.pagination  import PageNumberPagination
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from .serializers import LikesSerializer
from posts.models import Post
from authors.models import Author
from .models import Likes
from rest_framework import status
from rest_framework.decorators import action

# from backend.likes import serializers


class LikesPagination(PageNumberPagination):
    page_size_query_param = 'size'
    page_query_param = 'page'

    def get_paginated_response(self, data):
        if not data:
            message = "object is empty!"
            return Response({"message": message}, status=status.HTTP_204_NO_CONTENT)
        return Response({'type': "Like", 'items': data})

class LikesRetrievedViewSet(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    pagination_class = LikesPagination
    serializer_class = LikesSerializer


    def get_queryset(self):
        targetUrl = str(self.request.build_absolute_uri())[:-6].replace("/api", "")
        return Likes.objects.filter(object=targetUrl)

class LikesViewSet(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    pagination_class = LikesPagination
    serializer_class = LikesSerializer


    def get_queryset(self):
        targetUrl = str(self.request.build_absolute_uri())[:-6].replace("/api", "")
        return Likes.objects.filter(object=targetUrl)
        
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        author = get_object_or_404(Author, local_id=self.kwargs["author"])
        serializer.save(author_url=author.id)

    
    @action(detail=False, methods=['POST'], url_path="decrement", url_name="decrement")
    def decrement(self, request, **kwargs):
        targetUrl = str(request.build_absolute_uri())[:-16].replace("/api", "")
        delete_request = Likes.objects.get(object=targetUrl)
        delete_request.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


    def get_permissions(self):
        """Manages Permissions On A Per-Action Basis"""
        if self.action in ['update', 'create', 'partial_update', 'destroy']:
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]

class LikesCommentViewSet(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    pagination_class = LikesPagination
    serializer_class = LikesSerializer


    def get_queryset(self):
        targetUrl = str(self.request.build_absolute_uri())[:-6].replace("/api", "")
        #check if object is not empty
        return Likes.objects.filter(object=targetUrl)


    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        author = get_object_or_404(Author, local_id=self.kwargs["author"])
        serializer.save(author_url=author.id)
    
    @action(detail=False, methods=['POST'], url_path="decrement", url_name="decrement")
    def decrement(self, request, **kwargs):
        targetUrl = str(request.build_absolute_uri())[:-16].replace("/api", "")
        delete_request = Likes.objects.get(object=targetUrl)
        delete_request.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get_permissions(self):
        """Manages Permissions On A Per-Action Basis"""
        if self.action in ['update', 'create', 'partial_update', 'destroy']:
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]