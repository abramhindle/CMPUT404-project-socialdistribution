from django.shortcuts import get_object_or_404
from concurrent.futures import ThreadPoolExecutor
from rest_framework import status
from .serializers import FollowerSerializer, FollowingSerializer
from rest_framework.response import Response
from .models import Follower, Following
from backend.helpers import get_author, get
from authors.models import Author
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.authentication import BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
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
@authentication_classes([TokenAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def friends_list(request, author):
    author_object: Author = get_object_or_404(Author, local_id=author)
    urls = [f"{author_object.id.rstrip('/')}/followers/", f"{author_object.id.rstrip('/')}/following/"]
    with ThreadPoolExecutor(max_workers=1) as executor:
        future = executor.map(lambda url: get(url), urls)
    futures = [f for f in future]
    followers = futures[0].json()["items"] if futures[0].status_code == 200 and "items" in futures[0].json() else []
    following = futures[1].json()["items"] if futures[1].status_code == 200 and "items" in futures[1].json() else []
    following_ids = list(map(lambda x: x["id"], following))
    friends = [follower for follower in followers if follower["id"] in following_ids]
    return Response({"type": "friends", "items": friends}, content_type="application/json")


@api_view(['GET'])
@authentication_classes([TokenAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def followers_list(request, author):
    author_object = get_object_or_404(Author, local_id=author)
    with ThreadPoolExecutor(max_workers=1) as executor:
        future = executor.map(lambda x: get_author(x), [f.actor for f in author_object.follower_set.all()])
    followers = [f for f in future if "type" in f]
    followers.sort(key=lambda x: x["displayName"])
    return Response({"type": "followers", "items": followers}, content_type="application/json")


@api_view(['GET', 'PUT', 'DELETE'])
@authentication_classes([TokenAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def followers_detail(request, author, follower):
    author_object = get_object_or_404(Author, local_id=author)
    if request.method == 'GET':
        author_followers = [f.actor for f in author_object.follower_set.all() if f.actor == follower]
        if len(author_followers) > 0:
            return Response({"ok": f"{author_object.displayName} Follows {author_followers[0]}!"}, status=status.HTTP_200_OK, content_type="application/json")
        return Response(status=status.HTTP_404_NOT_FOUND)
    elif request.method == 'PUT':
        follower_json = get_author(follower)
        if "displayName" in follower_json:
            summary = f"{follower_json['displayName']} Wants To Follow {author_object.displayName}"
            follower_object = Follower(summary=summary, object=author_object, actor=follower)
            if len(Follower.objects.filter(object=author_object, actor=follower)) == 0:
                follower_object.save()
            else:
                follower_object = Follower.objects.get(object=author_object, actor=follower)
            return Response(FollowerSerializer(follower_object).data, content_type="application/json")
        return Response({"error": "Follower Does Not Exist!"}, content_type="application/json", status=status.HTTP_404_NOT_FOUND)
    follower_object = get_object_or_404(Follower, object=author_object, actor=follower)
    follower_object.delete()
    return Response(content_type="application/json", status=status.HTTP_204_NO_CONTENT)


@api_view(['PUT', 'DELETE'])
@authentication_classes([TokenAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def following_detail(request, author, following):
    author_object = get_object_or_404(Author, local_id=author)
    if request.method == 'PUT':
        following_json = get_author(following)
        if "displayName" in following_json:
            following_object = Following(author=author_object, follows=following)
            if len(Following.objects.filter(author=author_object, follows=following)) == 0:
                following_object.save()
            else:
                following_object = Following.objects.get(author=author_object, follows=following)
            return Response(FollowingSerializer(following_object).data, content_type="application/json")
        return Response({"error": "Following Does Not Exist!"}, content_type="application/json", status=status.HTTP_404_NOT_FOUND)
    following_object = get_object_or_404(Following, author=author_object, follows=following)
    following_object.delete()
    return Response(content_type="application/json", status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
@authentication_classes([TokenAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def following_list(request, author):
    author_object = get_object_or_404(Author, local_id=author)
    with ThreadPoolExecutor(max_workers=1) as executor:
        future_1 = executor.map(lambda x: get_author(x), [f.follows for f in author_object.following_set.all()])
    following = [f for f in future_1 if "id" in f]
    with ThreadPoolExecutor(max_workers=1) as executor:
        future_2 = executor.map(lambda x: get(x), [f"{f['id']}followers/{author_object.id}/" for f in following])
    confirmed_following = [f[0] for f in zip(following, [f for f in future_2]) if f[1] is not None and f[1].status_code != 404]
    confirmed_following.sort(key=lambda x: x["displayName"])
    return Response({"type": "following", "items": confirmed_following}, content_type="application/json")
