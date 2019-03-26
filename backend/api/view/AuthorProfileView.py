from urllib.parse import urlparse

from django.db import transaction
from rest_framework import generics
from rest_framework import authentication, permissions, status
from ..serializers import AuthorProfileSerializer
from rest_framework.response import Response
from ..models import AuthorProfile, Follow, ServerUser
import uuid
import requests
import json
from django.conf import settings


class AuthorProfileView(generics.GenericAPIView):
    serializer_class = AuthorProfileSerializer
    permission_classes = (permissions.IsAuthenticated,)
    mutable_keys = ["displayName", "github", "bio", "firstName", "lastName", "email"]

    def is_mutable(self, key):
        for ele in self.mutable_keys:
            if (key == ele):
                return True
        return False

    def post(self, request, uid):
        authorId = self.kwargs['uid']

        if (authorId == ""):
            return Response("Error: Author ID required!", status.HTTP_400_BAD_REQUEST)

        else:
            try:
                author_to_update = AuthorProfile.objects.filter(id=uid)
                if (not author_to_update.exists()):
                    return Response("Error: Author does not exist", status.HTTP_400_BAD_REQUEST)
                author_to_update = author_to_update[0]
                if (request.user.authorprofile.id != author_to_update.id):
                    return Response("Error: You do not have permission to edit this profile",
                                    status.HTTP_400_BAD_REQUEST)
                else:
                    for key, value in request.data.items():
                        if self.is_mutable(str(key)):
                            if (value == None):
                                error_message = "Error: {} cannot have value as None".format(key)
                                return Response(error_message, status.HTTP_400_BAD_REQUEST)
                            setattr(author_to_update, key, value)
                        else:
                            error_message = "Error: Can't modify {}".format(key)
                            return Response(error_message, status.HTTP_400_BAD_REQUEST)

                    author_to_update.full_clean()
                    author_to_update.save()
                    return Response("Success: Successfully updated profile", status.HTTP_200_OK)
            except:
                return Response("Error: Update Profile Fail", status.HTTP_400_BAD_REQUEST)

    def get(self, request, uid):
        authorId = self.kwargs['uid']
        if (authorId == ""):
            return Response("Error: Author ID required!", status.HTTP_400_BAD_REQUEST)

        author_profile_exists = AuthorProfile.objects.filter(user=request.user).exists()
        server_user_exists = ServerUser.objects.filter(user=request.user).exists()

        # from front end
        if author_profile_exists:
            is_local_uuid = True
            # for foreign author:
            # expect front end to send http://127.0.0.1:8000/author/http%3A%2F%2F127.0.0.1%3A1234%2Fauthor%2F163974c0-b350-4e9b-a708-b570acee826d
            # for local author:
            # expect to front end to send http://127.0.0.1:8000/author/163974c0-b350-4e9b-a708-b570acee826d
            try:
                uuid.UUID(uid)
            except ValueError:
                is_local_uuid = False
            if is_local_uuid:
                try:
                    author_profile = AuthorProfile.objects.get(id=authorId)
                    response_data = AuthorProfileSerializer(author_profile).data
                    friends = Follow.objects.filter(authorA=response_data["id"], status="FRIENDS")
                    friends_list_data = []
                    for ele in friends:
                        friend_fulll_id = ele.authorB
                        tmp = friend_fulll_id.split("author/")
                        friend_host = tmp[0]
                        friend_short_id = tmp[1]

                        if (ServerUser.objects.filter(host=friend_host).exists()):
                            try:
                                server_user = ServerUser.objects.get(host=friend_host)
                                url = "{}api/author/{}".format(server_user.host, friend_short_id)
                                my_cross_server_username = settings.USERNAME
                                my_cross_server_password = settings.PASSWORD
                                headers = {'Content-type': 'application/json'}
                                response = requests.get(url,
                                                        auth=(my_cross_server_username, my_cross_server_password),
                                                        headers=headers)
                                if response.status_code == 200:
                                    friends_list_data.append(json.loads(response.content))
                            except Exception as e:
                                # ignore and just not add into friend list if cant get from server
                                pass

                        else:
                            friend_profile = AuthorProfile.objects.get(id=friend_short_id)
                            serialized_author_profile = AuthorProfileSerializer(friend_profile)
                            friends_list_data.append(serialized_author_profile.data)

                    response_data["friends"] = friends_list_data

                    return Response(response_data, status.HTTP_200_OK)
                except:
                    return Response("Author does not exist", status.HTTP_400_BAD_REQUEST)
            # front end requesting foreign authors
            else:
                try:
                    parsed_url = urlparse(authorId)

                    foreign_server = ServerUser.objects.get(
                        host="{}://{}/".format(parsed_url.scheme, parsed_url.netloc))

                    url = "{}api{}".format(foreign_server.host, parsed_url.path)
                    my_cross_server_username = settings.USERNAME
                    my_cross_server_password = settings.PASSWORD
                    headers = {'Content-type': 'application/json'}
                    response = requests.get(url,
                                            auth=(my_cross_server_username, my_cross_server_password),
                                            headers=headers)
                    if (response.status_code == 200):
                        response_data = json.loads(response.content)
                        return Response(response_data, status.HTTP_200_OK)
                    else:
                        return Response("Get author profile from foreign host failed", status.HTTP_400_BAD_REQUEST)
                except ServerUser.DoesNotExist:
                    return Response("Author not from allowed host", status.HTTP_400_BAD_REQUEST)
        # when server make the request
        elif server_user_exists:
            try:
                author_profile = AuthorProfile.objects.get(id=authorId)
                response_data = AuthorProfileSerializer(author_profile).data
                return Response(response_data, status.HTTP_200_OK)
            except:
                return Response("Author does not exist", status.HTTP_400_BAD_REQUEST)
        else:
            return Response("Request not from invalid place", status.HTTP_400_BAD_REQUEST)
