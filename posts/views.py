from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions

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
        try:
            post = Post.objects.get(pk=post_id)
        except Post.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = PostSerializer(post, many=False)
        return Response(serializer.data)
    
    """
    Update the post
    """
    def post(self, request, author_id, post_id):
        # author_id not really needed as post_id should be unique by itself
        try:
            post = Post.objects.get(pk=post_id)
        except Post.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        serializer = PostSerializer(post, data=request.data, partial=True)
        if serializer.is_valid():
            post = serializer.save()
            post.update_fields_with_request(request)
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)