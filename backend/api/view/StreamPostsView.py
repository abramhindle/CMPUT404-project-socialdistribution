from django.db import transaction
from rest_framework import generics
from rest_framework import authentication, permissions, status
from ..serializers import AuthorProfileSerializer, PostSerializer
from rest_framework.response import Response
from ..models import AuthorProfile, Follow, Post, ServerUser
from .Util import *
import requests
import json
from urllib.parse import urlparse


class StreamPostsView(generics.GenericAPIView):
    serializer_class = AuthorProfileSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def handle_comments_origin(self, user_id, posts, friend_list):
        stream = []
        for post in posts:
            if (can_read(user_id, post, friend_list)):
                stream.append(build_post(post))
        return stream

    def get_local_posts(self, user_id, friend_list_data):
        query_set = Post.objects.all()
        stream_posts = PostSerializer(query_set, many=True).data

        return self.handle_comments_origin(user_id, stream_posts, friend_list_data)

    def get(self, request):

        author_profile_exists = AuthorProfile.objects.filter(user=request.user).exists()
        server_user_exists = ServerUser.objects.filter(user=request.user).exists()
        stream = []

        if not (server_user_exists or author_profile_exists):
            return Response("Invalid request user", status.HTTP_400_BAD_REQUEST)

        if author_profile_exists:
            user_profile = AuthorProfile.objects.get(user=request.user)
            user_id = get_author_id(user_profile, False)
            friend_list_data = get_local_friends_list(user_id)
            posts = self.get_local_posts(user_id, friend_list_data)

            for server_user in ServerUser.objects.all():
                headers = {'Content-type': 'application/json',
                           "X-Request-User-ID": user_id}
                url = "{}{}author/posts".format(server_user.host, server_user.prefix)
                response = requests.get(url,
                                        auth=(server_user.send_username, server_user.send_password),
                                        headers=headers)
                if response.status_code == 200:
                    response_json = json.loads(response.content)
                    posts += response_json["posts"]

        elif server_user_exists:
            user_id = request.META["HTTP_X_REQUEST_USER_ID"]
            friend_list_data = get_foreign_friend_list(user_id)
            posts = self.get_local_posts(user_id, friend_list_data)
        else:
            return Response("Error: invalid host", status.HTTP_400_BAD_REQUEST)

        sorted_stream = sorted(posts, key=lambda k: k['published'], reverse=True)

        response_data = {
            "query": "posts",
            "count": len(sorted_stream),
            "posts": sorted_stream
        }
        return Response(response_data, status.HTTP_200_OK)

        #
        # try:
        #     if ServerUser.objects.filter(user=request.user).exists():
        #         user_id = request.META["HTTP_X_REQUEST_USER_ID"]
        #         query_set = Post.objects.none()
        #         friend_list_data = get_foreign_friend_list(user_id)
        #     else:
        #         user_profile = AuthorProfile.objects.get(user=request.user)
        #         # getting all post made by the authenticated user first since they show up in the stream too
        #         query_set = Post.objects.filter(author=user_profile)
        #         user_id = get_author_id(user_profile, False)
        #         friend_list_data = get_local_friends_list(user_id)
        #
        #     authors_followed = Follow.objects.filter(authorA=user_id)
        #
        #     foreign_hosts = []
        #     for author in authors_followed:
        #         author_uuid = get_author_profile_uuid(author.authorB)
        #         try:
        #             author_profile = AuthorProfile.objects.get(id=author_uuid)
        #             query_set = query_set | Post.objects.filter(author=author_profile)
        #         except:
        #             # add foreign host to list to get it latter
        #             parsed_url = urlparse(author.authorB)
        #             author_host = '{}://{}/'.format(parsed_url.scheme, parsed_url.netloc)
        #             if author_host not in foreign_hosts:
        #                 foreign_hosts.append(author_host)
        #
        #     query_set = query_set.order_by("-published")
        #     stream_posts = PostSerializer(query_set, many=True).data
        #     stream = []
        #     for post in stream_posts:
        #         if (can_read(user_id, post, friend_list_data)):
        #             stream.append(post)
        # except:
        #     return Response("Author does not exist", status.HTTP_400_BAD_REQUEST)
        #
        # # if request is not forwarded
        # if not ServerUser.objects.filter(user=request.user).exists():
        #     for foreign_host in foreign_hosts:
        #         try:
        #             server_user = ServerUser.objects.get(host=foreign_host)
        #             headers = {'Content-type': 'application/json',
        #                        "X-Request-User-ID": AuthorProfileSerializer(user_profile).data["id"]}
        #             url = "{}{}author/posts".format(server_user.host, server_user.prefix)
        #             response = requests.get(url,
        #                                     auth=(server_user.send_username, server_user.send_password),
        #                                     headers=headers)
        #
        #             if response.status_code == 200:
        #                 response_json = json.loads(response.content)
        #                 stream += response_json["posts"]
        #         except ServerUser.DoesNotExist:
        #             return Response("Get request fail, bad foreign host",
        #                             status.HTTP_400_BAD_REQUEST)
        #         except Exception as e:
        #             pass
        #             # return Response("Error: Get foreign author post failed", status.HTTP_400_BAD_REQUEST)
        #
        # sorted_stream = sorted(stream, key=lambda k: k['published'], reverse=True)
        #
        # response_data = {
        #     "query": "posts",
        #     "count": len(sorted_stream),
        #     "posts": sorted_stream
        # }
        #
        # return Response(response_data, status.HTTP_200_OK)
