from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from .models import Post
from authors.models import Author
from .serializers import PostSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from backend.permissions import IsOwnerOrAdmin


class IsPostOwnerOrAdmin(IsOwnerOrAdmin):
    """Only Allow Owners Or Admins To Access The Object"""

    @staticmethod
    def get_owner(obj):
        return obj.author.profile


class CustomPageNumberPagination(PageNumberPagination):
    page_size_query_param = 'size'

    def get_paginated_response(self, data):
        return Response({'type': "posts", 'items': data})


class PostViewSet(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    pagination_class = CustomPageNumberPagination
    serializer_class = PostSerializer

    def get_queryset(self):
        author = self.kwargs["author"]
        return Post.objects.filter(author__local_id=author).order_by("-published")

    def perform_create(self, serializer):
        author = get_object_or_404(Author, local_id=self.kwargs["author"])
        serializer.save(author=author)

    def get_permissions(self):
        """Manages Permissions On A Per-Action Basis"""
        if self.action in ['update', 'create', 'partial_update', 'destroy']:
            permission_classes = [IsAuthenticated, IsPostOwnerOrAdmin]
        else:
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]
