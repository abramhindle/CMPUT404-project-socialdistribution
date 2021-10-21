from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, ListCreateAPIView
from rest_framework.response import Response
from rest_framework import status, permissions

from authors.models import Author
from authors.serializers import AuthorSerializer
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
            author_id = kwargs.get("author_id")
            _ = Author.objects.get(pk=author_id)
            self.posts = Post.objects.filter(
                author_id=author_id
            ).order_by('-published')
        except (KeyError, Author.DoesNotExist):
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

    """
    get comments of the post
    """
    def get(self, request, *args, **kwargs):
        try:
            post_id = kwargs.get("post_id")
            _ = Post.objects.get(pk=post_id)
            self.comments = Comment.objects.filter(
                post_id=post_id
            ).order_by('-published')    
        except (KeyError, Post.DoesNotExist):
            return Response(status=status.HTTP_404_NOT_FOUND)
 
        response = super().list(request, *args, **kwargs)
        return response

    """
    add comment to the post
    """
    def post(self, request, author_id, post_id):
        # check if the post and post's author exist
        try:
            _ = Author.objects.get(pk=author_id)
            post = Post.objects.get(pk=post_id)
            comment_author_json = request.data.pop("author")
            comment_author_url = comment_author_json["url"]
        except (Author.DoesNotExist, Post.DoesNotExist):
            error_msg = "Cannot find either the author or post id"
            return Response(error_msg, status=status.HTTP_404_NOT_FOUND)
        except KeyError:
            # the author and author.url attributes must exist
            # otherwise we have no idea who made the comment
            error_msg = "Payload must contain author and author.url attribute"
            return Response(error_msg, status=status.HTTP_400_BAD_REQUEST)

        comment_author_set = Author.objects.filter(url=comment_author_url)
        # check if author is local
        if comment_author_set and comment_author_set.get().is_internal():
            # local author
            comment_author = comment_author_set.get()
        else:
            # foreign author
            comment_author_serializer = AuthorSerializer(data=comment_author_json)
            if not comment_author_serializer.is_valid():
                return Response(comment_author_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            comment_author = comment_author_serializer.upcreate_from_validated_data()

        comment_serializer = CommentSerializer(data=request.data)
        if comment_serializer.is_valid():
            comment = Comment.objects.create(
                author=comment_author, 
                post=post,
                **comment_serializer.validated_data
            )
            comment.update_fields_with_request(request)
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(comment_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CommentDetail(APIView):
    def get_serializer_class(self):
        return CommentSerializer

    """
    get the comment with the specific post and author
    """
    def get(self, request, author_id, post_id, comment_id):
        try:
            comment = Comment.objects.get(pk=comment_id)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
    
        serializer = CommentSerializer(comment, many=False)
        return Response(serializer.data)