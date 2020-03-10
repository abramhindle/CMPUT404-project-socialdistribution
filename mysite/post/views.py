from django.db.models import Q
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import (
    IsAuthenticated,
    AllowAny,
    IsAdminUser,
    IsAuthenticatedOrReadOnly,
)
from rest_framework.decorators import action

from user.models import User
from friend.models import Friend
from comment.models import Comment
from comment.serializer import CommentSerializer
from .serializers import PostSerializer
from .models import Post, VISIBILITYCHOICES
from .permissions import OwnerOrAdminPermissions


class PostsViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    lookup_field = "id"

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_queryset(self):
        # 1 visibility="PUBLIC"
        q1 = Q(visibility="PUBLIC")

        if self.request.user.is_authenticated:
            # 2 visibility="FOAF"
            user_f2_ids = self.request.user.f1Ids.filter(status="A").values_list(
                "f2Id", flat=True
            )
            user_f1_ids = self.request.user.f2Ids.filter(status="A").values_list(
                "f1Id", flat=True
            )
            friends_usernames = list(user_f2_ids) + list(user_f1_ids)
            f2_foaf = Friend.objects.filter(
                Q(status="A") & Q(f1Id__in=list(friends_usernames))
            ).values_list("f2Id", flat=True)
            f1_foaf = Friend.objects.filter(
                Q(status="A") & Q(f2Id__in=list(friends_usernames))
            ).values_list("f1Id", flat=True)
            foaf = list(f1_foaf) + list(f2_foaf)
            q2_1 = Q(visibility="FOAF")
            q2_2 = Q(author__username__in=foaf)

            # 3 visibility="FRIENDS"
            user_f2_ids = self.request.user.f1Ids.filter(status="A").values_list(
                "f2Id", flat=True
            )
            user_f1_ids = self.request.user.f2Ids.filter(status="A").values_list(
                "f1Id", flat=True
            )
            friends = list(user_f2_ids) + list(user_f1_ids)
            q3_1 = Q(visibility="FRIENDS")
            q3_2 = Q(author__username__in=friends)

            # q4: post is private but user is in post's visiableTo list.
            q4_1 = Q(visibility="PRIVATE")
            q4_2 = Q(
                visibleTo__contains=self.request.user.username
            )  # check if Json string contains user's email.

            # q5: post's author is the user
            q5 = Q(author=self.request.user)

            visible_posts = Post.objects.filter(
                q1 | (q2_1 & q2_2) | (q3_1 & q3_2) | (q4_1 & q4_2) | q5
            )
        else:  # anonymous user
            visible_posts = Post.objects.filter(q1)

        return visible_posts

    def get_permissions(self):
        if self.action in ["update", "destroy", "partial_update", "create"]:
            self.permission_classes = [
                OwnerOrAdminPermissions,
            ]
        else:
            self.permission_classes = [AllowAny]
        return super(PostsViewSet, self).get_permissions()

    @action(detail=True, methods=["GET"])
    def get_comments(self, request, *args, **kwargs):
        post = self.get_object()
        comments = Comment.objects.filter(post=post)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data, status=200)

    @action(detail=True, methods=["POST"])
    def post_comment(self, request, *args, **kwargs):
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
