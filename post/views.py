from django.shortcuts import render
from django.db.models import Subquery
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Post, Like, Comment
from .serializers import PostSerializer, LikeSerializer

import json
# Create your views here.

class index(APIView):
    def get(self,request,author_id):
        post_ids = Post.objects.filter(ownerID=author_id)
        if not post_ids:
            return Response(status = 404)
        serializer = PostSerializer(post_ids, many=True)
        response = {'type':'posts', 'items': serializer.data}
        return Response(response)

class comments(APIView):
    pass

# all owners posts
class post(APIView):

    def get(self,request,author_id, post_id):
        post_ids = Post.objects.filter(ownerID=author_id, postID=post_id)
        if not post_ids:
            return Response(status = 404)

        serializer = PostSerializer(post_ids, many=True)
        response = {'type':'posts', 'items': serializer.data}
        return Response(response)

    def post():
        pass

    def put():
        pass

    def delete():
        pass

class likes(APIView):
    def get(self,request,author_id,post_id):
        likes = Like.objects.filter(authorID=author_id,postID=post_id)
        if not likes:
            return Response(status = 404) #consider replacing with no likes for this post
        serializer = LikeSerializer(likes,many = True)
        response = {'type':'likes','items': serializer.data}
        return Response(response)
class commentLikes(APIView):
    pass
