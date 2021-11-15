from django.shortcuts import render
from django.views import generic
from django.shortcuts import render
from django.template import loader
from django.http.request import HttpRequest
from .models import Post
from apps.core.models import Author
from django.core import serializers
import json

def index(request: HttpRequest):
    posts = Post.objects.all()
    template = loader.get_template('posts/index.html')
    context = {'posts': posts,}
    return render(request, 'posts/index.html', context)

def makepost(request: HttpRequest):
    template= loader.get_template('posts/makepost.html')
    currentAuthor=Author.objects.filter(userId=request.user).first()
    context = {'author' : currentAuthor}
    print(serializers.serialize('json',[currentAuthor]))
    return render(request,'posts/makepost.html',context)
