from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from socialdistribution.models import *
from socialdistribution.serializers import *

@api_view(['GET'])
def like_post_view(request, author_write_article_ID, postID):
    if request.method == "GET":
        likes = LikePost.objects.filter(postID=postID)
        serializer = LikePostSerializer(likes,many=True)
        return Response(serializer.data)


@api_view(['GET'])
def like_comment_view(request, author_write_article_ID, commentID,postID):
    if request.method == "GET":
        likes = LikeComment.objects.filter(commentID=commentID)
        serializer = LikeCommentSerializer(likes,many=True)
        return Response(serializer.data)

@api_view(['GET'])
def liked_view(request,authorID):
    if request.method == "GET":
        likeds = Liked.objects.filter(authorID=authorID)
        serializer = LikedSerializer(likeds,many=True)
        return Response(serializer.data)
