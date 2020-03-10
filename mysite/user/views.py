from django.db.models import Q
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import (
    IsAuthenticated,
    AllowAny,
    IsAdminUser,
    IsAuthenticatedOrReadOnly,
)

from friend.models import Friend
from post.models import Post
from post.serializers import PostSerializer
from .serializers import AuthorSerializer
from .models import User
from .permissions import OwnerOrAdminPermissions

# Create your views here.
class AuthorViewSet(viewsets.ModelViewSet):
    serializer_class = AuthorSerializer
    queryset = User.objects.filter(is_superuser=0)
    lookup_field = "username"

    def get_permissions(self):
        if self.action in ["update", "destroy", "partial_update", "create"]:
            # user can only use this view with valid token
            self.permission_classes = [OwnerOrAdminPermissions]
        else:
            self.permission_classes = [AllowAny]
        return super(AuthorViewSet, self).get_permissions()

    @action(detail=True, methods=["GET"])
    def user_posts(self, request, *args, **kwargs):
        author = self.get_object()
        author_posts = Post.objects.filter(author=author)

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

            posts = author_posts.filter(
                q1 | (q2_1 & q2_2) | (q3_1 & q3_2) | (q4_1 & q4_2)
            )
        else:  # anonymous user
            posts = Post.objects.filter(q1)
        serializer = PostSerializer(posts, many=True)

        return Response(serializer.data, status=200)

    @action(detail=False, methods=["GET"])
    def current_user(self, request, *args, **kwargs):
        if request.user.is_anonymous:
            return Response(status=401)
        serializer = AuthorSerializer(self.request.user)
        return Response(serializer.data, status=200)
