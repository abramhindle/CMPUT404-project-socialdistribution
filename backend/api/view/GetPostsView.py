import uuid

from rest_framework import generics, permissions, status
from rest_framework.response import Response
from ..models import Post, AuthorProfile, ServerUser
from ..serializers import PostSerializer, AuthorProfileSerializer
from .Util import *
import requests
import json


class GetPostsView(generics.GenericAPIView):
    serializer_class = AuthorProfileSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_local_author_post(self, request_user_full_id, author_id):
        try:
            author_profile = AuthorProfile.objects.get(id=author_id)
        except AuthorProfile.DoesNotExist:
            return Response("Error: Author does not exist!", status.HTTP_400_BAD_REQUEST)

        author_posts = Post.objects.filter(author=author_profile).order_by("-published")

        author_full_id = get_author_id(author_profile, False)

        is_own_posts_author = str(author_full_id) == str(request_user_full_id)
        posts = PostSerializer(author_posts, many=True).data
        posts_response = []

        for post in posts:
            if(can_read(request_user_full_id, post) or is_own_posts_author):
                comments = []
                for comment in post["comments"]:
                    author_id = comment["author"]
                    author_uuid = get_author_profile_uuid(author_id)
                    local_commenting_author = AuthorProfile.objects.filter(id=author_uuid)

                    if(local_commenting_author.exists()):
                        print("save me")
                        local_author = local_commenting_author[0]
                        author = AuthorProfileSerializer(local_author).data
                        comment["author"] = author
                        comments.append(comment)
                    elif(not local_commenting_author.exists()):
                         # forward the request
                        parsed_post_url = urlparse(comment["author"])
                        commenter_host = '{}://{}/'.format(parsed_post_url.scheme, parsed_post_url.netloc)
                        headers = {'Content-type': 'application/json'}
                        try:
                            server_obj = ServerUser.objects.get(host=commenter_host)
                            commenter_short_id = get_author_profile_uuid(comment["author"])
                            url = "{}api/author/{}".format(server_obj.host, commenter_short_id)
                            response = requests.get(url,
                                                    auth=(server_obj.send_username, server_obj.send_password),
                                                    headers=headers
                                                    )
                            if(response.status_code != 200):
                                return Response("Error: Unable to get foreign profile", status.HTTP_400_BAD_REQUEST)
                            
                            else:
                                print(response," freedom")

                                response_json = json.loads(response.content)
                                comment["author"] = response_json
                                comments.append(comment)
                        except ServerUser.DoesNotExist:
                            return Response("Error: Author not from allowed host", status.HTTP_400_BAD_REQUEST)
                        except Exception as e:
                            return Response(e,status.HTTP_400_BAD_REQUEST)
                    else:
                        return Response("Error: unable to fetch comments for post", status.HTTP_400_BAD_REQUEST)
                post["comments"] = comments
                posts_response.append(post)
        response_data = {
            "query": "posts",
            "count": len(posts_response),
            "posts": posts_response
        }
        return Response(response_data, status.HTTP_200_OK)


    def get(self, request, authorid):
        author_id = self.kwargs['authorid']
        if(author_id == ""):
            status_code = status.HTTP_400_BAD_REQUEST
            return Response("Error: no author id was specified", status_code)

        author_profile_exists = AuthorProfile.objects.filter(user=request.user).exists()
        server_user_exists = ServerUser.objects.filter(user=request.user).exists()

        # from front end
        if author_profile_exists:
            is_local_uuid = True
            # for foreign author:
            # expect front end to send http://127.0.0.1:8000/api/author/http%3A%2F%2F127.0.0.1%3A1234%2Fapi%2Fauthor%2F163974c0-b350-4e9b-a708-b570acee826d/posts
            # for local author:
            # expect to front end to send http://127.0.0.1:8000/api/author/163974c0-b350-4e9b-a708-b570acee826d/posts
            try:
                uuid.UUID(author_id)
            except ValueError:
                is_local_uuid = False

            if is_local_uuid:
                user_profile = AuthorProfile.objects.get(user=request.user)
                request_user_full_id = get_author_id(user_profile, False)
                return self.get_local_author_post(request_user_full_id, author_id)

            # front end requesting foreign authors
            else:
                try:
                    parsed_url = urlparse(author_id)
                    foreign_server = ServerUser.objects.get(host="{}://{}/".format(parsed_url.scheme, parsed_url.netloc))
                    short_foreign_author_id = author_id.split("author/")[-1]
                    url = "{}{}author/{}/posts".format(foreign_server.host, foreign_server.prefix, short_foreign_author_id)
                    user_profile = AuthorProfile.objects.get(user=request.user)
                    headers = {'Content-type': 'application/json',
                               "X-Request-User-ID": AuthorProfileSerializer(user_profile).data["id"]}
                    response = requests.get(url,
                                            auth=(foreign_server.send_username, foreign_server.send_password),
                                            headers=headers)
                    if (response.status_code == 200):
                        return Response(response.json(), status.HTTP_200_OK)
                    else:
                        return Response("Error: Get foreign author post failed", status.HTTP_400_BAD_REQUEST)
                except ServerUser.DoesNotExist:
                    return Response("Error: Request not from allowed host", status.HTTP_400_BAD_REQUEST)
                except Exception as e:
                    return Response("Error: Get foreign author post failed", status.HTTP_400_BAD_REQUEST)
        # when server make the request
        elif server_user_exists:
            request_user_full_id = request.META.get("HTTP_X_REQUEST_USER_ID", "")
            return self.get_local_author_post(request_user_full_id, author_id)
        else:
            return Response("Request not from valid server", status.HTTP_400_BAD_REQUEST)


