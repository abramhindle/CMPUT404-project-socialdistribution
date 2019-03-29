from rest_framework import generics, permissions, status
from rest_framework.response import Response
from ..models import Post, AuthorProfile, Comment, ServerUser
from ..serializers import PostSerializer, AuthorProfileSerializer, CommentSerializer
from .Util import *
import json
from django.conf import settings
import requests

class PostCommentsView(generics.GenericAPIView):
    serializer_class = AuthorProfileSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def valid_payload(self, request):
        # try:
        #     query_valid = data["query"] == "addComment" 
        #     comment_valid_id = len(data["post"]) != 0
        #     comment_valid_host = len(data["comment"]["author"]) == 0
        #     comment_valid_displayname = len(data["author"]["displayName"]) == 0
        #     comment_valid_url = len(data["author"]["url"]) != 0
        #     comment_valid_comment = len(data["comment"]) != 0 
        #     comment_valid_ct = len(data["contentType"]) != 0

        #     if (query_valid or 
        #         comment_valid_id or
        #         comment_valid_host or
        #         comment_valid_displayname or
        #         comment_valid_url or
        #         comment_valid_comment or 
        #         comment_valid_ct
        #     ):
        #         return False
        # except:
        #     return False
        return True

    def insert_local_comment(self, request):
        post_data = request.data["post"]
        post_data_split = post_data.split("/")
        # from server
        post_short_id = post_data_split[-1]
        local_post_filter = Post.objects.filter(id=str(post_short_id))
        if(local_post_filter.exists()):
            author_post = local_post_filter[0]

            author_data = request.data["comment"]["author"]["id"].split("/")

            if(can_read(str(author_data[-1]), PostSerializer(author_post).data)):

                Comment.objects.create(
                            author=request.data["comment"]["author"]["id"],
                            comment=request.data["comment"]["comment"],
                            contentType=request.data["comment"]["contentType"],
                            post=author_post
                        )

                response_obj = {
                    "query": "addComment",
                    "success": True,
                    "message": "Comment Added"
                }
                return Response(response_obj, status.HTTP_200_OK)

            else:
                response_obj = {
                    "query": "addComment",
                    "success": False,
                    "message":"Comment not allowed"
                }
                return Response(response_obj, status.HTTP_403_FORBIDDEN)

    def post(self, request, postid):
        if (postid == ""):
            return Response("Error: Post ID must be specified", status.HTTP_400_BAD_REQUEST)

        if(not self.valid_payload(request.data)):
            return Response("Error: Payload does not match", status.HTTP_400_BAD_REQUEST)
        else:
            author_profile_filter = AuthorProfile.objects.filter(user=request.user)
            server_user_exists = ServerUser.objects.filter(user=request.user).exists()

            if(author_profile_filter.exists()):
                # request is from front end
                author_profile = author_profile_filter[0]
                payload_author_id = request.data["comment"]["author"]["id"]
                requesting_author_id = get_author_id(author_profile, False)
                
                if(payload_author_id != requesting_author_id):
                    return Response("Error: Payload author and requesting author does not match", status.HTTP_400_BAD_REQUEST)
                # check if the post is foreign or local

                parsed_post_url = urlparse(request.data["post"])

                post_host = '{}://{}/'.format(parsed_post_url.scheme, parsed_post_url.netloc)
                if(author_profile.host != post_host):
                    # forward the request
                    headers = {'Content-type': 'application/json'}

                    try:
                        server_obj = ServerUser.objects.get(host=post_host)
                        url = "{}{}posts/{}/comments".format(server_obj.host, server_obj.prefix, postid)
                        response = requests.post(url,
                                                auth=(server_obj.send_username, server_obj.send_password),
                                                headers=headers,
                                                data=json.dumps(request.data)
                                                )
                        return Response(response.json(), response.status_code)
                    except ServerUser.DoesNotExist:
                        return Response("Error: Author not from allowed host", status.HTTP_400_BAD_REQUEST)
                    except Exception as e:
                        return Response(e,status.HTTP_400_BAD_REQUEST)
                else:
                    return self.insert_local_comment(request)
            elif(server_user_exists):
                return self.insert_local_comment(request)
            else:
                return Response("Error: Request not from allowed hosts", status.HTTP_400_BAD_REQUEST)
 