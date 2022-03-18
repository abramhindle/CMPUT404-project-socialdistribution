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


class LikesPagination(PageNumberPagination):
    page_size_query_param = 'size'
    page_query_param = 'page'

    def get_paginated_response(self, data):
        return Response({'type': "Like", 'items': data})


class LikesViewSet(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    pagination_class = LikesPagination
    serializer_class = LikesSerializer

    def get_queryset(self):
        post = self.kwargs["post"]
        return Likes.objects.filter(post__local_id=post)

    def perform_create(self, serializer):
        post = get_object_or_404(Post, local_id=self.kwargs["post"])
        author = get_object_or_404(Author, local_id=self.kwargs["author"])
        serializer.save(author_url=author.id, post=post)

    def get_permissions(self):
        """Manages Permissions On A Per-Action Basis"""
        if self.action in ['update', 'create', 'partial_update', 'destroy']:
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]
