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
    
    """
    Delete the post
    """
    def delete(self, request, author_id, post_id): 
        try:
            post = Post.objects.get(pk=post_id)
        except Post.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    """
    Create a Post with the post_id
    """
    def put(self, request, author_id, post_id):
        # check whether post with that id already exist
        # and check whether the author exist
        try:
            _ = Post.objects.get(pk=post_id)
            return Response(status=status.HTTP_409_CONFLICT)
        except Post.DoesNotExist:
            try:
                author = Author.objects.get(pk=author_id)
            except Author.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            # conversion from camelCase to snake_case
            # and get the value (e.g. "PUB") from the label (e.g. "PUBLIC")
            request.data["content_type"] = Post.ContentType[request.data.pop("contentType")]
            request.data["visibility"] = Post.Visibility[request.data["visibility"]]
            post = Post.objects.create(
                author=author, 
                id=post_id,
                **request.data
            )
            post.update_fields_with_request(request)
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
