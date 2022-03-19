from django.shortcuts import get_object_or_404
from concurrent.futures import ThreadPoolExecutor
from rest_framework import viewsets
from rest_framework import status
import requests as r
from .serializers import FollowerSerializer, FollowingSerializer
import json
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from .models import Follower, Following
from authors.models import Author
from rest_framework.decorators import api_view, throttle_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from backend.permissions import IsOwnerOrAdmin


class IsFollowerOwnerOrAdmin(IsOwnerOrAdmin):
    """Only Allow Owners Or Admins To Access The Object"""

    @staticmethod
    def get_owner(obj: Follower):
        return obj.object.profile


class IsFollowingOwnerOrAdmin(IsOwnerOrAdmin):
    """Only Allow Owners Or Admins To Access The Object"""

    @staticmethod
    def get_owner(obj: Following):
        return obj.author.profile


@api_view(['GET'])
def followers_list(request, author):
    author_object = get_object_or_404(Author, local_id=author)
    with ThreadPoolExecutor(max_workers=1) as executor:
        future = executor.map(lambda x: r.get(x).json(), [f.actor for f in author_object.follower_set.all()])
    foreign_posts = [p for p in future if "type" in p]
    return Response({"type": "followers", "items": foreign_posts}, content_type="application/json")


@api_view(['GET', 'PUT', 'DELETE'])
def followers_detail(request, author, follower):
    author_object = get_object_or_404(Author, local_id=author)
    if request.method == 'GET':
        print(follower)
        author_followers = [f.actor for f in author_object.follower_set.all() if f.actor == follower]
        return Response({"ok": author_followers}, content_type="application/json")
    elif request.method == 'PUT':
        follower_json = r.get(follower).json()
        if "displayName" in follower_json:
            summary = f"{follower_json['displayName']} Wants To Follow {author_object.displayName}"
            follower_object = Follower(summary=summary, object=author_object, actor=follower)
            if len(Follower.objects.filter(actor=follower)) == 0:
                follower_object.save()
            else:
                follower_object = Follower.objects.get(actor=follower)
            return Response(FollowerSerializer(follower_object).data, content_type="application/json")
        return Response({"error": "Follower Does Not Exist!"}, content_type="application/json", status=status.HTTP_404_NOT_FOUND)
    follower_object = get_object_or_404(Follower, actor=follower)
    follower_object.delete()
    return Response(content_type="application/json", status=status.HTTP_204_NO_CONTENT)
