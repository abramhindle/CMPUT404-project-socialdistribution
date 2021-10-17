from django.shortcuts import render
from django.db.models import Subquery
from django.http import HttpResponse, http404
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

    def get(self,request,author_id, post_id):
        #url only has owner_id: want all posts of a user
        post_ids = None
        if not post_id:
            post_ids = Post.objects.filter(ownerID = owner_id)
            #nothing was returned for that user-Id
        #url has both owner_id and post_id: want specific post from a user
        elif post_id and owner_id:
            post_ids = Post.objects.filter(ownerID = owner_id, postID = post_id)
        
        if not post_ids:
            return Response(status = 404)

        serializer = PostSerializer(post_ids)
        response = {'type':'posts', 'items': serializer}
        return Response(response)
    
    def post():
        pass
    
    def put():
        pass

    def delete():
        pass

class likes(APIView):
    pass

#class commentLikes(APIView):
    #pass