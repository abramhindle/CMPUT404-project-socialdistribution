from rest_framework import generics, permissions, status
from rest_framework.response import Response
from ..models import Post, AuthorProfile, Comment
from ..serializers import PostSerializer, AuthorProfileSerializer, CommentSerializer
from .Util import *


class PostCommentsView(generics.GenericAPIView):
    serializer_class = AuthorProfileSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, postid):
        if (postid == ""):
            return Response("Error: Post ID must be specified", status.HTTP_400_BAD_REQUEST)
        else:
            post_id = self.kwargs["postid"]
            author_post = Post.objects.get(id=post_id)

            commenting_author = AuthorProfile.objects.get(user=request.user)
            request_user_full_id = get_author_id(commenting_author, False)
            if(not can_read(request_user_full_id, PostSerializer(author_post).data)):
                response_obj = {
                    "query": "addComment",
                    "success": False,
                    "message":"Comment not allowed"
                }
                return Response(response_obj, status.HTTP_403_FORBIDDEN)
            else:
                Comment.objects.create(
                            author=commenting_author,
                            comment=request.data["comment"],
                            contentType=request.data["contentType"],
                            post=author_post
                        )
                response_obj = {
                    "query": "addComment",
                    "success": True,
                    "message":"Comment Added"
                }
                return Response(response_obj, status.HTTP_200_OK)
