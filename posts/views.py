from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, ListCreateAPIView
from rest_framework.response import Response
from rest_framework import status, permissions

from authors.models import Author
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer
from .pagination import CommentsPagination, PostsPagination

import uuid
import copy

class PostDetail(APIView):
    def get_serializer_class(self):
        return PostSerializer

    """
    Get author post with the post_id
    """
    def get(self, request, author_id, post_id):
        try:
            post = Post.objects.get(pk=post_id)
        except Post.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        # TODO: what if the author itself want to get friends/private posts?
        if (post.visibility != Post.Visibility.PUBLIC):
            return Response(status=status.HTTP_403_FORBIDDEN)
    
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
            post = Post.objects.create(
                author=author, 
                id=post_id,
                **serializer.validated_data
            )
            post.update_fields_with_request(request)
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PostList(ListCreateAPIView):
    serializer_class = PostSerializer
    pagination_class = PostsPagination

    # used by the ListCreateAPIView super class 
    def get_queryset(self):
        return self.posts

    """
    Get recent posts of author (paginated)
    """
    def get(self, request, *args, **kwargs):
        try:
            self.posts = Post.objects.filter(
                author_id=kwargs.get("author_id")
            ).order_by('-published')
        except (KeyError, Post.DoesNotExist):
            return Response(status=status.HTTP_404_NOT_FOUND)
 
        response = super().list(request, *args, **kwargs)
        return response
    
    """
    Create a Post with generated post id
    """
    def post(self, request, author_id):
        post_id = uuid.uuid4()
        return PostDetail().put(request, author_id, post_id)

class CommentList(ListCreateAPIView):
    serializer_class = CommentSerializer
    pagination_class = CommentsPagination

    # used by the ListCreateAPIView super class 
    def get_queryset(self):
        return self.comments

    def get(self, request, *args, **kwargs):
        try:
            self.comments = Comment.objects.filter(
                post_id=kwargs.get("post_id")
            ).order_by('-published')
        except (KeyError, Post.DoesNotExist):
            return Response(status=status.HTTP_404_NOT_FOUND)
 
        response = super().list(request, *args, **kwargs)
        return response

    """
    add comment to the post
    """
    def post(self, request, author_id, post_id):
        try:
            author = Author.objects.get(pk=author_id)
            post = Post.objects.get(pk=post_id)
        except (Author.DoesNotExist, Post.DoesNotExist):
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            comment = Comment.objects.create(
                author=author, 
                post=post,
                **serializer.validated_data
            )
            comment.update_fields_with_request(request)
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)