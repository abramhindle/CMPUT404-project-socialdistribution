from django.shortcuts import render
from django.views import generic
from django.shortcuts import render
from django.template import loader
from django.http.request import HttpRequest
from .models import Post

def index(request: HttpRequest):
    posts = Post.objects.all()
    template = loader.get_template('posts/index.html')
    context = {'posts': posts,}
    return render(request, 'posts/index.html', context)