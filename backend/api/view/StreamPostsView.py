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
            user_profile = AuthorProfile.objects.get(user=request.user)
            query_set = Post.objects.filter(author=user_profile)

            user_id = get_author_id(user_profile, False)
            authors_followed = Follow.objects.filter(authorA=user_id)
            
            for author in authors_followed:
                author_uuid = get_author_profile_uuid(author.authorB)
                author_profile = AuthorProfile.objects.get(id=author_uuid)
                query_set = query_set | Post.objects.filter(author=author_profile)

            query_set = query_set.order_by("-published")
            stream_posts = PostSerializer(query_set, many=True).data
            stream = []
            for post in stream_posts:
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