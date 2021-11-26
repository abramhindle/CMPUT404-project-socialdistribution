from django.shortcuts import render
from django.views import generic
from django.shortcuts import render
from django.template import loader
from django.http.request import HttpRequest
import uuid

from apis.posts.views import post
from .models import Post
from .models import Comment
from apps.core.models import Author
from django.core import serializers
from apps.core.serializers import AuthorSerializer
from socialdistribution.utils import Utils
import json

def index(request: HttpRequest):
    if request.user.is_anonymous:
        return render(request,'core/index.html')
    currentAuthor=Author.objects.filter(userId=request.user).first()
    posts = Post.objects.filter(author=currentAuthor)
    print(posts[0].id)
    get_comments()
    template = loader.get_template('posts/index.html')
    context = {'posts': posts,}
    return render(request, 'posts/index.html', context)

def makepost(request: HttpRequest):
    template= loader.get_template('posts/makepost.html')
    currentAuthor=Author.objects.filter(userId=request.user).first()
    host = request.scheme + "://" + request.get_host()
    context = {'author' : currentAuthor, 'host' : host}
    return render(request,'posts/makepost.html',context)

def editpost(request: HttpRequest):
    template= loader.get_template('posts/editpost.html')
    currentAuthor=Author.objects.filter(userId=request.user).first()
    currentAuthorPosts = Post.objects.filter(author=currentAuthor)
    currentAuthorPostList = []
    for post in currentAuthorPosts:
        currentAuthorPostList.append(post)
    host = request.scheme + "://" + request.get_host()
    context = {'author' : currentAuthor, 'posts': currentAuthorPosts, 'host':host}
    return render(request,'posts/editpost.html',context)

def get_comments():
    id = "d57bbd0e-185c-4964-9e2e-d5bb3c02841a"
    comments = Comment.objects.filter(post= id)
    print(comments)
#     return comments