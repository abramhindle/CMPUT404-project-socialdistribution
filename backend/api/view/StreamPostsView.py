from django.db import transaction
from rest_framework import generics
from rest_framework import authentication, permissions, status
from ..serializers import AuthorProfileSerializer, PostSerializer
from rest_framework.response import Response
from ..models import AuthorProfile, Follow, Post
from .Util import *

class StreamPostsView(generics.GenericAPIView):

    serializer_class = AuthorProfileSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        #if they were able to log in, then they can access the end point

        try:
            #GET ALL POSTS
            stream_posts = Post.objects.all().order_by("-published")
            posts = PostSerializer(stream_posts, many=True).data
            stream = []

            for post in posts:
                if(can_read(request, post)):
                    # print(post, "\n")
                    stream.append(post)

            response_data = {
                    "query": "posts",
                    "count": len(stream),
                    "posts": stream
                }

            return Response(response_data, status.HTTP_200_OK)
        except:
            return Response("Author does not exist", status.HTTP_400_BAD_REQUEST)