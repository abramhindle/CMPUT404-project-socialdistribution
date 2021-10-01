from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response

from authors.models import Author
from .models import Post
from .serializers import PostSerializer

class PostDetail(APIView):
    def get_serializer_class(self):
        return PostSerializer

    """
    Get author posts
    """
    def get(self, request, author_id, post_id):
        # author_id not really needed as post_id should be unique by itself
        post = Post.objects.get(pk=post_id)
        serializer = PostSerializer(post, many=False)
        return Response(serializer.data)
