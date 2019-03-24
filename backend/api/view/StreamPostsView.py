from urllib.parse import urlparse

from django.db import transaction
from rest_framework import generics
from rest_framework import authentication, permissions, status
from ..serializers import AuthorProfileSerializer, PostSerializer
from rest_framework.response import Response
from ..models import AuthorProfile, Follow, Post, ServerUser
from .Util import *
import requests
import json


class StreamPostsView(generics.GenericAPIView):
    serializer_class = AuthorProfileSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):

        author_profile_exists = AuthorProfile.objects.filter(user=request.user).exists()
        server_user_exists = ServerUser.objects.filter(user=request.user).exists()

        if not (server_user_exists or author_profile_exists):
            return Response("Get Request Fail", status.HTTP_400_BAD_REQUEST)

        try:
            if ServerUser.objects.filter(user=request.user).exists():
                user_id = request.META["HTTP_X_REQUEST_USER_ID"]
                query_set = Post.objects.none()
            else:
                user_profile = AuthorProfile.objects.get(user=request.user)
                # getting all post made by the authenticated user first since they show up in the stream too
                query_set = Post.objects.filter(author=user_profile)
                user_id = get_author_id(user_profile, False)

            authors_followed = Follow.objects.filter(authorA=user_id)

            foreign_hosts = []
            for author in authors_followed:
                print(author)
                author_uuid = get_author_profile_uuid(author.authorB)
                try:
                    author_profile = AuthorProfile.objects.get(id=author_uuid)
                    print(author_profile)
                    query_set = query_set | Post.objects.filter(author=author_profile)
                except AuthorProfile.DoesNotExist:
                    print("got foreign")
                    parsed_url = urlparse(author.authorB)
                    author_host = '{}://{}/'.format(parsed_url.scheme, parsed_url.netloc)
                    if author_host not in foreign_hosts:
                        foreign_hosts.append(author_host)

            query_set = query_set.order_by("-published")
            stream_posts = PostSerializer(query_set, many=True).data
            stream = []
            for post in stream_posts:
                if (can_read(user_id, post)):
                    stream.append(post)
        except:
            return Response("Author does not exist", status.HTTP_400_BAD_REQUEST)

        print(foreign_hosts)
        print(not ServerUser.objects.filter(user=request.user).exists())
        # if request is not forwarded
        if not ServerUser.objects.filter(user=request.user).exists():
            for foreign_host in foreign_hosts:
                try:
                    server_user = ServerUser.objects.get(host=foreign_host)
                    headers = {'Content-type': 'application/json',
                               "X-Request-User-ID": AuthorProfileSerializer(user_profile).data["id"]}
                    url = server_user.host + "api/author/posts"
                    my_cross_server_username = settings.USERNAME
                    my_cross_server_password = settings.PASSWORD
                    response = requests.get(url, auth=(my_cross_server_username, my_cross_server_password),
                                            headers=headers)
                    if response.status_code != 200:
                        print(response.content)
                        return Response("Cross Server get post Request Fail", status.HTTP_400_BAD_REQUEST)
                    else:
                        response_json = json.loads(response.content)
                        stream += response_json["posts"]
                except ServerUser.DoesNotExist:
                    return Response("Get request fail, bad foreign host",
                                    status.HTTP_400_BAD_REQUEST)

        sorted_stream = sorted(stream, key=lambda k: k['published'], reverse=True)

        response_data = {
            "query": "posts",
            "count": len(sorted_stream),
            "posts": sorted_stream
        }

        return Response(response_data, status.HTTP_200_OK)
