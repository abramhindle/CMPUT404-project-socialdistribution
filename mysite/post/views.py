from django.db.models import Q
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import (
    IsAuthenticated,
    AllowAny,
    IsAdminUser,
    IsAuthenticatedOrReadOnly,
)
from rest_framework.decorators import action

from user.models import User
from user.serializers import AuthorSerializer
from comment.models import Comment
from comment.serializer import CommentSerializer
from .serializers import PostSerializer
from .models import Post, VISIBILITYCHOICES
from .permissions import OwnerOrAdminPermissions


# Create your views here.
class UserPostsViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    lookup_field = "id"

    def get_permissions(self):
        if self.action in ["update", "destroy", "partial_update", "create"]:
            self.permission_classes = [
                OwnerOrAdminPermissions,
            ]
        else:
            self.permission_classes = [AllowAny]
        return super(UserPostsViewSet, self).get_permissions()

    def get_queryset(self):
        return self.request.user.posts.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=True, methods=["GET"])
    def getComments(self, request, *args, **kwargs):
        post = self.get_object()
        comments = Comment.objects.filter(post=post)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data, status=200)

    @action(detail=True, methods=["POST"])
    def postComment(self, request, *args, **kwargs):
        post = self.get_object()
        data = request.data
        data["created_by"] = request.user.username
        data["post"] = post.id
        serializer = CommentSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class VisiblePostsViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    lookup_field = "id"

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_queryset(self):
        q1 = Q(visibility="PUBLIC")
        if self.request.user.is_authenticated:
            # To be done
            # q2 = Q(visibility = "FOAF")
            # q3_1 = Q(visibility="Friends")
            # q3_2 = Q(author.friends)
            # q4: post is private but user is in post's visiableTo list.
            q4_1 = Q(visibility="PRIVATE")
            q4_2 = Q(
                visibleTo__contains=self.request.user.username
            )  # check if Json string contains user's email.
            # q5: post's author is the user
            q5 = Q(author=self.request.user)
            return Post.objects.filter(q1 | (q4_1 & q4_2) | q5)
        else:  # anonymous user
            return Post.objects.filter(q1)

    def get_permissions(self):
        if self.action in ["update", "destroy", "partial_update", "create"]:
            self.permission_classes = [
                OwnerOrAdminPermissions,
            ]
        else:
            self.permission_classes = [AllowAny]
        return super(VisiblePostsViewSet, self).get_permissions()

    @action(detail=True, methods=["GET"])
    def getComments(self, request, *args, **kwargs):
        post = self.get_object()
        comments = Comment.objects.filter(post=post)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data, status=200)

    @action(detail=True, methods=["POST"])
    def postComment(self, request, *args, **kwargs):
        post = self.get_object()
        data = request.data
        data["created_by"] = request.user.username
        data["post"] = post.id
        serializer = CommentSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


# To be done
# class ServerPostViewSet(viewsets.ModelViewSet):
