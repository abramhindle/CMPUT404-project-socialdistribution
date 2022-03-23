from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from .models import Post
from authors.models import Author
from .serializers import PostSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import action
import base64
from rest_framework.authentication import TokenAuthentication, BasicAuthentication
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
    authentication_classes = [TokenAuthentication, BasicAuthentication]
    pagination_class = CustomPageNumberPagination
    serializer_class = PostSerializer

    @action(detail=True, methods=['GET'])
    def image(self, request, author, pk):
        print(request.headers)
        post: Post = get_object_or_404(Post, local_id=pk)
        string = post.content
        content = string.split("base64,")[1]
        mimetype = string.split(";base64,")[0].split(":")[1]
        response = HttpResponse(content_type=mimetype)
        response.write(base64.b64decode(content))
        return response

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
        elif self.action in ["image"]:
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
