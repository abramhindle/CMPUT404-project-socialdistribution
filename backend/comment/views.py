from rest_framework.pagination import PageNumberPagination
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication, BasicAuthentication
from .serializers import CommentSerializer
from posts.models import Post
from .models import Comment
from backend.permissions import IsOwnerOrAdmin
from rest_framework.decorators import action
from likes.models import Likes
from likes.helper import get_likes


class IsPostOwnerOrAdmin(IsOwnerOrAdmin):
    """Only Allow Owners Or Admins To Access The Object"""

    @staticmethod
    def get_owner(obj: Comment):
        return obj.post.author.profile


class CommentPagination(PageNumberPagination):
    page_size_query_param = 'size'
    page_query_param = 'page'

    def get_paginated_response(self, data):
        return Response({'type': "comments", 'items': data})


class CommentViewSet(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication, BasicAuthentication]
    pagination_class = CommentPagination
    serializer_class = CommentSerializer
    parser_classes = [JSONParser]

    @action(detail=True, methods=['GET'])
    def likes(self, request, author, post, pk):
        comment: Comment = get_object_or_404(Comment, local_id=pk)
        likes = Likes.objects.all().filter(object=comment.id)
        return Response(get_likes(likes), content_type="application/json")

    def get_queryset(self):
        post = self.kwargs["post"]
        return Comment.objects.filter(post__local_id=post).order_by("published")

    def perform_create(self, serializer):
        post = get_object_or_404(Post, local_id=self.kwargs["post"])
        serializer.save(author_url=self.request.data["author"]["url"], post=post)

    def get_permissions(self):
        """Manages Permissions On A Per-Action Basis"""
        if self.action in ['update', 'partial_update', 'destroy']:
            permission_classes = [IsAuthenticated, IsOwnerOrAdmin]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
