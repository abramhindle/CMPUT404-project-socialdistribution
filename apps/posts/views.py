from django.shortcuts import render
from django.views import generic
from django.shortcuts import render
from django.template import loader
from django.http.request import HttpRequest

from apis.posts.views import post
from .models import Post
from .models import Like
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

def get_comments(post_id):
    comments = Comment.objects.filter(post=post_id)
    return comments

def get_likes_post(post_id):
    likes = Like.objects.filter(post= post_id)
    return likes

def get_likes_comments(comment_id):
    likes = Like.objects.filter(comment= comment_id)