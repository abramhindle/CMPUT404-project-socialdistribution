from django.shortcuts import render
from django.db.models import Subquery
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Post, Like, Comment
from .serializers import PostSerializer
import json
# Create your views here.

class index(APIView):
    pass

class comments(APIView):
    pass

# all owners posts
class post(APIView):
    def getPosts(self,request,owner_id):
        post_ids = Post.objects.filter(ownerID = owner_id)
        if not post_ids:
            return Response(status = 404)
        serializer = PostSerializer(post_ids)
        response = {'type':'posts', 'items': serializer}
        return Response(response)

    def getPost(self, request, owner_id, post_id):
        post_ids = Post.objects.filter(ownerID = owner_id, postID = post_id)
        if not post_ids:
            return Response(status = 404)
        serializer = PostSerializer(post_ids)
        response = {'type':'posts', 'items': serializer}
        return Response(response)

class likes(APIView):
    pass

#class commentLikes(APIView):
    #pass