from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions

from authors.models import Author
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer

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

class PostList(APIView):
    def get_serializer_class(self):
        return PostSerializer

    # """
    # Get recent posts of author (paginated)
    # """
    # TODO:
    # def get(self, request, author_id):
    #     pass
    
    """
    Create a Post with generated post id
    """
    def post(self, request, author_id):
        post_id = uuid.uuid4()
        return PostDetail().put(request, author_id, post_id)

class CommentDetail(APIView):
    def get_serializer_class(self):
        return CommentSerializer

    """
    get comments of the post
    """
    def get(self, request, author_id, post_id):
        try:
            comments = Comment.objects.filter(post_id=post_id).order_by('-published')
        except Post.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        params = request.query_params.dict()
        try:
            # defaulting to page 1 with size 20
            page = int(params["page"]) if "page" in params else 1
            size = int(params["size"]) if "size" in params else 20
        except ValueError:
            # page and size must be integers
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
        serializer = CommentSerializer(comments, many=True)
        lower_index = (page - 1) * size
        upper_index = page * size
        if (lower_index >= len(serializer.data)):
            # when requesting pages that are out of bound
            return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.data[lower_index:upper_index])
    
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