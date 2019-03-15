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
        try:
            stream_posts = Post.objects.all().order_by("-published")
            user_profile = AuthorProfile.objects.get(user=request.user)
            user_id = get_author_id(user_profile, False)
            authors_followed = Follow.objects.filter(authorA=user_id).values('authorB')
            authors_followed = list(authors_followed)

            authors_followed.append({"authorB": user_id})
            stream = []
            posts = PostSerializer(stream_posts, many=True).data
            for author in authors_followed: 
                for post in posts:
                    isFollowingOrOwnPost = post["author"]["id"] == author["authorB"]
                    if(isFollowingOrOwnPost):
                        if(can_read(request, post)):
                            stream.append(post)

            response_data = {
                    "query": "posts",
                    "count": len(stream),
                    "posts": stream
                }

            return Response(response_data, status.HTTP_200_OK)
        except:
            return Response("Author does not exist", status.HTTP_400_BAD_REQUEST)