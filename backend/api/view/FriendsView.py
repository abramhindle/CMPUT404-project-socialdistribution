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
        query_valid = len(data["query"]) == 0
        author_valid_id = len(data["author"]["id"]) == 0
        author_valid_host = len(data["author"]["host"]) == 0
        author_valid_displayname = len(data["author"]["displayName"]) == 0
        author_valid_url = len(data["author"]["url"]) == 0
        friend_valid_id = len(data["friend"]["id"]) == 0
        friend_valid_host = len(data["friend"]["host"]) == 0
        friend_valid_displayname = len(data["friend"]["displayName"]) == 0
        friend_valid_url = len(data["friend"]["url"]) == 0

        if (query_valid or
        author_valid_id or
        author_valid_host or
        author_valid_displayname or
        author_valid_url or
        friend_valid_id or
        friend_valid_host or
        friend_valid_displayname or
        friend_valid_url
        ):
            return False
    except:
        return False
    return True


def valid_local_author(author_host, author_id):
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
    #print(request.data["friend"]["host"])
    author_profile_exists = AuthorProfile.objects.filter(user=request.user).exists()
    server_user_exists = ServerUser.objects.filter(user=request.user).exists()
    parsed_url = urlparse(request.data["author"]["id"])
    author_host = '{}://{}/'.format(parsed_url.scheme, parsed_url.netloc)
    parsed_url = urlparse(request.data["friend"]["id"])
    friend_host = '{}://{}/'.format(parsed_url.scheme, parsed_url.netloc)
    # when request comes from frontend
    if author_profile_exists:
        # validate author in "author"
        if not valid_local_author(author_host,
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
                response = requests.post(url,
                                         data=payload,
                                         auth=(server_user.send_username, server_user.send_password),
                                         headers=headers)
                if response.status_code != 200:
                    return Response(response.json(), status.HTTP_400_BAD_REQUEST)
            except ServerUser.DoesNotExist:
                return Response("Follow Request Fail, author in 'friend' is not in the allowed host",
                                status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                return Response("Error: Remote friend request failed", status.HTTP_400_BAD_REQUEST)

        else:
            # validate author in "friend"
            if not valid_local_author(friend_host,
                                      request.data["friend"]["id"]):
                return Response("Follow Request Fail, author in 'friend' does not exist",
                                status.HTTP_400_BAD_REQUEST)
    # when request comes from other servers
    elif server_user_exists:
        # check host 2 exist
        if not valid_local_author(friend_host,
                                  request.data["friend"]["id"]):
            return Response("Follow Request Fail, author in 'friend' does not exist",
                            status.HTTP_400_BAD_REQUEST)
    else:
        return Response("Follow Request Fail", status.HTTP_400_BAD_REQUEST)

    existing_follow = Follow.objects.filter(authorA=request.data["friend"]["id"],
                                            authorB=request.data["author"]["id"],
                                            status="FOLLOWING")

    existing_friend = Follow.objects.filter(authorA=request.data["friend"]["id"],
                                            authorB=request.data["author"]["id"],
                                            status="FRIENDS")

    if existing_friend:
        return Response("Already Friends", status.HTTP_200_OK)

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

def unfollow_user_update(author, friend):

    existing_follow = Follow.objects.filter(authorA=author,
                                            authorB=friend)
    if (existing_follow.exists()):
        if (existing_follow[0].status == "FRIENDS"):
            existing_friend = Follow.objects.get(authorA=friend,
                                                    authorB=author,
                                                    status="FRIENDS")
            setattr(existing_friend, "status", "FOLLOWING")
            existing_friend.save()
        existing_follow.delete()
        return Response("Unfollow Request Success", status.HTTP_200_OK)
    else:
        return Response("Unfollow Request Fail", status.HTTP_400_BAD_REQUEST)

def valid_foreign_author(author_host, author_id):

    try:
        tmp = author_id.split("author/")
        author_short_id = tmp[1]
        server_user = ServerUser.objects.get(host=author_host)
        headers = {'Content-type': 'application/json'}
        url = "{}{}author/{}".format(server_user.host, server_user.prefix, author_short_id)
        response = requests.get(url, 
                                auth=(server_user.send_username, 
                                server_user.send_password), 
                                headers=headers)
        if(response.status_code == 200):
            return True
        else:
            return False
    except:
        return False

    

# function to unfollow
def unfollow(request):
    author_profile_exists = AuthorProfile.objects.filter(user=request.user).exists()
    server_user_exists = ServerUser.objects.filter(user=request.user).exists()
    parsed_url = urlparse(request.data["author"]["id"])
    author_host = '{}://{}/'.format(parsed_url.scheme, parsed_url.netloc)
    author_id = request.data["author"]["id"]
    parsed_url = urlparse(request.data["friend"]["id"])
    friend_host = '{}://{}/'.format(parsed_url.scheme, parsed_url.netloc)
    friend_id = request.data["friend"]["id"]

    if author_profile_exists:
        check_author = valid_local_author(author_host, author_id)
        if(not check_author):
            return Response("Local author does not exist", status.HTTP_400_BAD_REQUEST)

        if(author_host != friend_host):
            
            check_foreign = valid_foreign_author(friend_host, friend_id)
            if((not check_foreign) and server_user_exists):
                return Response("Foreign author does not exist", status.HTTP_400_BAD_REQUEST)

            try:
                server_user = ServerUser.objects.get(host=friend_host)
                headers = {'Content-type': 'application/json'}
                url = "{}{}unfollow".format(server_user.host, server_user.prefix)
                response = requests.post(url, 
                                        auth=(server_user.send_username, 
                                        server_user.send_password), 
                                        headers=headers, 
                                        data=json.dumps(request.data))
                if(response.status_code == 200):
                    return unfollow_user_update(author_id,friend_id)
                else:
                    print(response.json())
                    return Response("Error: Foreign server failed to unfollow", status.HTTP_400_BAD_REQUEST)
            except:
                return Response("Error: foreign server not allowed", status.HTTP_400_BAD_REQUEST)
        else:
            check_author = valid_local_author(friend_host, friend_id)
            if(not check_author):
                return Response("Local friend does not exist", status.HTTP_400_BAD_REQUEST)
            return unfollow_user_update(author_id,friend_id)

    elif server_user_exists:
        check_author = valid_foreign_author(author_host, author_id)
        if(not check_author):
            return Response("Foreign author does not exist", status.HTTP_400_BAD_REQUEST)

        check_friend = valid_local_author(friend_host, friend_id)
        if(not check_friend):
            return Response("Local friend does not exist", status.HTTP_400_BAD_REQUEST)
       
        return unfollow_user_update(author_id,friend_id)
    else:
        return Response("Failed to unfriend", status.HTTP_400_BAD_REQUEST)


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
