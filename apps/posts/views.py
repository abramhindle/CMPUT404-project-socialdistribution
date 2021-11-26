from django.shortcuts import render, redirect
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
    
    # should include friends etc at some points
    posts = Post.objects.filter(visibility="PUBLIC")
    template = loader.get_template('posts/index.html')
    host = request.scheme + "://" + request.get_host()
    context = {'posts': posts,'host':host}
    return render(request, 'posts/index.html', context)

def my_posts(request: HttpRequest):
    if request.user.is_anonymous or not (request.user.is_authenticated):
        return render(request,'posts/index.html')
    currentAuthor=Author.objects.filter(userId=request.user).first()
    posts = Post.objects.filter(author=currentAuthor)
    template = loader.get_template('posts/index.html')
    host = request.scheme + "://" + request.get_host()
    context = {'posts': posts,'host':host, 'author': currentAuthor}
    return render(request, 'posts/index.html', context)

def makepost(request: HttpRequest):
    if request.user.is_anonymous or not (request.user.is_authenticated):
        return render(request,'posts/makepost.html')
    template= loader.get_template('posts/makepost.html')
    currentAuthor=Author.objects.filter(userId=request.user).first()
    host = request.scheme + "://" + request.get_host()
    context = {'author' : currentAuthor, 'host' : host}
    return render(request,'posts/makepost.html',context)

def editpost(request: HttpRequest, post_id: str):
    if request.user.is_anonymous or not (request.user.is_authenticated):
        return render(request,'posts/editpost.html')
    template= loader.get_template('posts/editpost.html')
    currentAuthor=Author.objects.filter(userId=request.user).first()
    post = Post.objects.get(pk=post_id)
    host = request.scheme + "://" + request.get_host()
    context = {'author' : currentAuthor, 'post': post, 'host':host}
    return render(request,'posts/editpost.html',context)

def deletepost(request: HttpRequest, post_id: str):
    if request.user.is_anonymous or not (request.user.is_authenticated):
        return render(request,'posts/index.html')
    currentAuthor=Author.objects.filter(userId=request.user).first()
    post = Post.objects.get(pk=post_id)
    if post.author.id == currentAuthor.id:
        post.delete()
    return redirect('posts:index')
