from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from socialdistribution.models import Post, Author,Comment,LikePost
from socialdistribution.serializers import LikePostSerializer

@api_view(['GET','POST'])
def like_post_view(request, author_write_article_ID, postID):
    if request.method == "GET":
        likes = LikePost.objects.filter(postID=postID)
        serializer = LikePostSerializer(likes,many=True)
        return Response(serializer.data)

    elif request.method == "POST":
        # create a new like
        data = request.data
        data['author_write_article_ID'] = author_write_article_ID
        data['postID'] = postID
        serializer = LikePostSerializer(data=data)
        if serializer.is_valid():
            like = serializer.save()
            return Response({"likeID":like.likeID}, status=status.HTTP_201_CREATED)
        return Response({'message':serializer.errors}, status=status.HTTP_400_BAD_REQUEST)