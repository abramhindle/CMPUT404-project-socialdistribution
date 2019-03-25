from urllib.parse import urlparse

from rest_framework import generics, permissions, status
from rest_framework.response import Response
from ..serializers import AuthorProfileSerializer
from ..models import Follow, AuthorProfile, ServerUser
import requests
import json
from django.conf import settings


def valid_input(data):
    try:
        if (len(data["query"]) == 0 or
                len(data["author"]["id"]) == 0 or
                len(data["friend"]["id"]) == 0):
            return False
    except:
        return False
    return True


def valid_author(request):
    try:
        tmp = request.data["author"]["id"].split("author/")
        author_host = tmp[0]
        # todo check if host is local when cross server
        author_short_id = tmp[1]

        tmp = request.data["friend"]["id"].split("author/")
        friend_host = tmp[0]
        # todo check if host is local when cross server
        friend_short_id = tmp[1]

        request_user = AuthorProfile.objects.filter(user=request.user)
        if not (request_user.exists() and
                AuthorProfile.objects.filter(id=friend_short_id).exists() and
                str(request_user[0].id) == str(author_short_id)):
            return False
    except:
        return False
    return True


def valid_local_author(request, author_host, author_id):
    try:
        tmp = author_id.split("author/")
        author_short_id = tmp[1]
        request_user = AuthorProfile.objects.filter(host=author_host, id=author_short_id)
        if not (request_user.exists()):
            return False
    except:
        return False
    return True


# function to follow or be friend
def follow(request):
    author_profile_exists = AuthorProfile.objects.filter(user=request.user).exists()
    server_user_exists = ServerUser.objects.filter(user=request.user).exists()

    parsed_url = urlparse(request.data["author"]["id"])
    author_host = '{}://{}/'.format(parsed_url.scheme, parsed_url.netloc)
    parsed_url = urlparse(request.data["friend"]["id"])
    friend_host = '{}://{}/'.format(parsed_url.scheme, parsed_url.netloc)

    # when request comes from frontend
    if author_profile_exists:
        # validate author in "author"
        if not valid_local_author(request,
                                  author_host,
                                  request.data["author"]["id"]):
            return Response("Follow Request Fail, author in 'author' does not exist",
                            status.HTTP_400_BAD_REQUEST)
        request_user_profile = AuthorProfile.objects.get(user=request.user)
        request_user_id = AuthorProfileSerializer(request_user_profile).data["id"]
        if(request_user_id != request.data["author"]["id"]):
            return Response("Follow Request Fail, cannot send friend request for other authors",
                            status.HTTP_400_BAD_REQUEST)

        if author_host != friend_host:
            try:
                server_user = ServerUser.objects.get(host=friend_host)
                payload = json.dumps(request.data)
                headers = {'Content-type': 'application/json'}
                url = "{}{}friendrequest".format(server_user.host, server_user.prefix)
                my_cross_server_username = settings.USERNAME
                my_cross_server_password = settings.PASSWORD
                response = requests.post(url, data=payload, auth=(my_cross_server_username, my_cross_server_password),
                                         headers=headers)
                if response.status_code != 200:
                    return Response("Cross Server Follow Request Fail", status.HTTP_400_BAD_REQUEST)
            except ServerUser.DoesNotExist:
                return Response("Follow Request Fail, author in 'friend' is not in the allowed host",
                                status.HTTP_400_BAD_REQUEST)
        else:
            # validate author in "friend"
            if not valid_local_author(request,
                                      friend_host,
                                      request.data["friend"]["id"]):
                return Response("Follow Request Fail, author in 'friend' does not exist",
                                status.HTTP_400_BAD_REQUEST)
    # when request comes from other servers
    elif server_user_exists:
        # check host 2 exist
        if not valid_local_author(request,
                                  friend_host,
                                  request.data["friend"]["id"]):
            return Response("Follow Request Fail, author in 'friend' does not exist",
                            status.HTTP_400_BAD_REQUEST)
    else:
        return Response("Follow Request Fail", status.HTTP_400_BAD_REQUEST)

    existing_follow = Follow.objects.filter(authorA=request.data["friend"]["id"],
                                            authorB=request.data["author"]["id"],
                                            status="FOLLOWING")
    if (existing_follow.exists()):
        Follow.objects.create(authorA=request.data["author"]["id"],
                              authorB=request.data["friend"]["id"],
                              status="FRIENDS")

        existing_follow.update(status="FRIENDS")
    else:
        # create if does not exist
        Follow.objects.get_or_create(authorA=request.data["author"]["id"],
                                     authorB=request.data["friend"]["id"],
                                     status="FOLLOWING")
    return Response("Follow Request Success", status.HTTP_200_OK)


# function to unfollow
def unfollow(request):
    if (valid_author(request)):
        existing_follow = Follow.objects.filter(authorA=request.data["author"]["id"],
                                                authorB=request.data["friend"]["id"])
        if (existing_follow.exists()):
            if (existing_follow[0].status == "FRIENDS"):
                existing_friend = Follow.objects.get(authorA=request.data["friend"]["id"],
                                                     authorB=request.data["author"]["id"],
                                                     status="FRIENDS")
                setattr(existing_friend, "status", "FOLLOWING")
                existing_friend.save()
            existing_follow.delete()

            return Response("Unfollow Request Success", status.HTTP_200_OK)
        else:
            return Response("Unfollow Request Fail", status.HTTP_400_BAD_REQUEST)
    else:
        return Response("Unfollow Request Fail", status.HTTP_400_BAD_REQUEST)


class FriendsView(generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        if (valid_input(request.data)):
            if (request.data["query"] == "friendrequest"):
                return follow(request)
            elif (request.data["query"] == "unfollow"):
                return unfollow(request)
            else:
                return Response('Invalid query type, must be "friendrequest" or "unfollow"',
                                status.HTTP_400_BAD_REQUEST)
        else:
            return Response("Invalid Input", status.HTTP_400_BAD_REQUEST)
