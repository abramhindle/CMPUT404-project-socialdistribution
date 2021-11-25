from django.shortcuts import render
from django.views import generic
from django.shortcuts import render
from django.template import loader
from django.http.request import HttpRequest
from .models import Post
from apps.core.models import Author
from django.core import serializers
from apps.core.serializers import AuthorSerializer
from socialdistribution.utils import Utils
import json

def index(request: HttpRequest):
    if request.user.is_anonymous or not (request.user.is_authenticated):
        return render(request,'posts/index.html')
    currentAuthor=Author.objects.filter(userId=request.user).first()
    posts = Post.objects.filter(author=currentAuthor)
    template = loader.get_template('posts/index.html')
    host = request.scheme + "://" + request.get_host()
    context = {'posts': posts,'host':host}
    return render(request, 'posts/index.html', context)

def makepost(request: HttpRequest):
    template= loader.get_template('posts/makepost.html')
    currentAuthor=Author.objects.filter(userId=request.user).first()
    host = request.scheme + "://" + request.get_host()
    context = {'author' : currentAuthor, 'host' : host}
    return render(request,'posts/makepost.html',context)

def editpost(request: HttpRequest, post_id: str):
    template= loader.get_template('posts/editpost.html')
    currentAuthor=Author.objects.filter(userId=request.user).first()
    post = Post.objects.get(pk=post_id)
    host = request.scheme + "://" + request.get_host()
    context = {'author' : currentAuthor, 'post': post, 'host':host}
    return render(request,'posts/editpost.html',context)
