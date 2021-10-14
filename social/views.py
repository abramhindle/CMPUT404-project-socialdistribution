from django.db.models.query_utils import refs_expression
from django.shortcuts import render

from rest_framework import viewsets
from django.shortcuts import render
from rest_framework import serializers
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.serializers import Serializer

from .serializers import AuthorSerializer, PostSerializer
from .models import Author, Post

# Create your views here.
@api_view(['GET'])
def author_view_api(request, id):
    try:
        author = Author.objects.get(id=id)
    except:
        return Response(status=404)
    
    if request.method == "GET":
        author_serializer = AuthorSerializer(author)
        author_dict = author_serializer.data
        author_dict["type"] = "author"
        return Response(author_dict)

@api_view(['GET'])
def authors_list_api(request):
    authors = list(Author.objects.all())

    author_serializer = AuthorSerializer(authors, many=True)
    authors_dict = {
        "type": "authors",
        "items": author_serializer.data
    }
    return Response(authors_dict)

@api_view(['GET'])
def follower_api(request, id, foreign_id=None):
    try:
        author = Author.objects.get(id=id)
    except:
        return Response(status=404)
    
    if foreign_id is not None:
        try:
            follower = author.followers.get(id=foreign_id)
        except:
            return Response(status=404)
        follower_serializer = AuthorSerializer(follower)
        follower_dict = follower_serializer.data
        follower_dict['type'] = "follower"
        return Response(follower_dict)

    followers = list(author.followers.all())
    follower_serializer = AuthorSerializer(followers, many=True)
    followers_dict = {
        "type": "followers",
        "items": follower_serializer.data
    }
    return Response(followers_dict)

@api_view(['GET'])
def post_view_api(request, id, post_id=None):
    try:
        author = Author.objects.get(id=id)
    except:
        return Response(status=404)
    
    if post_id is not None:
        try:
            post = Post.objects.get(id=post_id)
        except:
            return Response(status=404)
        
        post_serializer = PostSerializer(post)
        post_dict = post_serializer.data
        post_dict['type'] = "post" 
        return Response(post_dict)
    
    posts = list(author.posted.all())
    post_serializer = PostSerializer(posts, many=True)
    posts_dict = {
        "type": "post",
        "items": post_serializer.data
    }
    return Response(posts_dict)