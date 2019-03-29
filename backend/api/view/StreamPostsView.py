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
            return Response("Invalid request user", status.HTTP_400_BAD_REQUEST)

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
                author_uuid = get_author_profile_uuid(author.authorB)
                try:
                    author_profile = AuthorProfile.objects.get(id=author_uuid)
                    query_set = query_set | Post.objects.filter(author=author_profile)
                except:
                    parsed_url = urlparse(author.authorB)
                    author_host = '{}://{}/'.format(parsed_url.scheme, parsed_url.netloc)
                    if author_host not in foreign_hosts:
                        foreign_hosts.append(author_host)

            query_set = query_set.order_by("-published")
            stream_posts = PostSerializer(query_set, many=True).data
            stream = []
            for post in stream_posts:
                sorted_comments= sorted(post["comments"], key=lambda k: k['published'], reverse=True)
                comments = []
                if (can_read(user_id, post)):
                    for comment in sorted_comments:
                        parsed_post_url = urlparse(comment["author"])
                        commenter_host = '{}://{}/'.format(parsed_post_url.scheme, parsed_post_url.netloc)
                        #check if the user is a local author
                        # if (can_read(user_id, post)):
                            # parsed_post_url = urlparse(comment["author"])
                            # commenter_host = '{}://{}/'.format(parsed_post_url.scheme, parsed_post_url.netloc)
                        local_commenting_author = AuthorProfile.objects.filter(id=user_id)

                        # case of local author
                        if local_commenting_author.exists():
                            local_author = local_commenting_author[0]
                            author = AuthorProfileSerializer(local_author).data
                            comment["author"] = author
                            comments.append(comment)
                        elif not local_commenting_author.exists():
                            # forward the request
                            parsed_post_url = urlparse(comment["author"])
                            commenter_host = '{}://{}/'.format(parsed_post_url.scheme, parsed_post_url.netloc)
                            headers = {'Content-type': 'application/json'}
                            try:
                                server_obj = ServerUser.objects.get(host=commenter_host)
                                commenter_short_id = get_author_id(comment["author"])
                                url = "{}api/author/{}".format(server_obj.host, commenter_short_id)
                                response = requests.post(url,
                                                        auth=(server_obj.send_username, server_obj.send_password),
                                                        headers=headers,
                                                        data=json.dumps(request.data)
                                                        )
                                if(response.status_code != 200):
                                    return Response("Error: Unable to get foreign profile", status.HTTP_400_BAD_REQUEST)
                                
                                else:
                                    response_json = json.loads(response.content)
                                    comment["author"] = response_json["author"]
                                    comments.append(comment)
                            except ServerUser.DoesNotExist:
                                return Response("Error: Author not from allowed host", status.HTTP_400_BAD_REQUEST)
                            except Exception as e:
                                return Response(e,status.HTTP_400_BAD_REQUEST)
                        else:
                            return Response("Error: unable to fetch comments for post", status.HTTP_400_BAD_REQUEST)
                    post["comments"] = comments
                    stream.append(post)
                        #check for if the user is local or now
                    # if local_author.exists():
                    #     local_author = local_author[0]
                    #     author = AuthorProfileSerializer(local_author).data
                    #     comment["author"] = author
                    #     comments.append(comment)  
                    #     post["comments"] = sorted_comments
                    # if (can_read(user_id, post)):
                    #     stream.append(post)

                # local_author = AuthorProfile.objects.filter(user=request.user)
                # if local_author.exists():
                #     local_author = local_author[0]
                #     author = AuthorProfileSerializer(local_author).data
                #     comment["author"] = author
                #     comments.append(comment)  
                # post["comments"] = sorted_comments
                # if (can_read(user_id, post)):
                #     stream.append(post)
        except:
            return Response("Author does not exist", status.HTTP_400_BAD_REQUEST)

        # if request is not forwarded
        if not ServerUser.objects.filter(user=request.user).exists():
            for foreign_host in foreign_hosts:
                try:
                    server_user = ServerUser.objects.get(host=foreign_host)
                    headers = {'Content-type': 'application/json',
                               "X-Request-User-ID": AuthorProfileSerializer(user_profile).data["id"]}
                    url = "{}{}author/posts".format(server_user.host, server_user.prefix)
                    response = requests.get(url,
                                            auth=(server_user.send_username, server_user.send_password),
                                            headers=headers)

                    if response.status_code != 200:
                        return Response(response.json(), status.HTTP_400_BAD_REQUEST)
                    else:
                        response_json = json.loads(response.content)
                        stream += response_json["posts"]
                except ServerUser.DoesNotExist:
                    return Response("Get request fail, bad foreign host",
                                    status.HTTP_400_BAD_REQUEST)
                except Exception as e:
                    return Response(e,status.HTTP_400_BAD_REQUEST)

        sorted_stream = sorted(stream, key=lambda k: k['published'], reverse=True)

        response_data = {
            "query": "posts",
            "count": len(sorted_stream),
            "posts": sorted_stream
        }

        return Response(response_data, status.HTTP_200_OK)
