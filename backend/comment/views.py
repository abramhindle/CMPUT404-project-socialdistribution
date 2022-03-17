from rest_framework.pagination import PageNumberPagination
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from .serializers import CommentSerializer
from posts.models import Post
from authors.models import Author
from .models import Comment


class CommentPagination(PageNumberPagination):
    page_size_query_param = 'size'
    page_query_param = 'page'

    def get_paginated_response(self, data):
        return Response({'type': "comments", 'items': data})


class CommentViewSet(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    pagination_class = CommentPagination
    serializer_class = CommentSerializer
    parser_classes = [JSONParser]

    def get_queryset(self):
        post = self.kwargs["post"]
        return Comment.objects.filter(post__local_id=post).order_by("published")

    def perform_create(self, serializer):
        post = get_object_or_404(Post, local_id=self.kwargs["post"])
        serializer.save(author_url=self.request.data["author"]["url"], post=post)

    def get_permissions(self):
        """Manages Permissions On A Per-Action Basis"""
        if self.action in ['update', 'create', 'partial_update', 'destroy']:
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]
