from django.shortcuts import render, redirect
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
    # should include friends etc at some points
    posts = Post.objects.filter(unlisted=False, visibility="PUBLIC")
    # TODO does not produce proper comments comments and like counts to be used on the html
    for post in posts:
    #     comments = get_comments_lmtd(post.id)
        post.num_likes = len(get_likes_post(post.id))
    host = request.scheme + "://" + request.get_host()
    context = {
        'posts': posts,
        'host': host,
        # 'comments': comments,
        }
    return render(request, 'posts/index.html', context)

def my_posts(request: HttpRequest):
    if request.user.is_anonymous or not (request.user.is_authenticated):
        return render(request,'posts/index.html')

    currentAuthor = Author.objects.filter(userId=request.user).first()
    posts = Post.objects.filter(author=currentAuthor)
    for post in posts:
    #     comments = get_comments_lmtd(i.id)
        post.num_likes = len(get_likes_post(post.id))
    template = loader.get_template('posts/index.html')
    host = request.scheme + "://" + request.get_host()
    context = {
        'posts': posts,
        'host': host,
        'author': currentAuthor,
        # 'comments': comments,
        }
    return render(request, 'posts/index.html', context)

def makepost(request: HttpRequest):
    if request.user.is_anonymous or not (request.user.is_authenticated):
        return render(request,'posts/makepost.html')
    template= loader.get_template('posts/makepost.html')
    currentAuthor=Author.objects.filter(userId=request.user).first()
    host = request.scheme + "://" + request.get_host()
    context = {'author' : currentAuthor, 'host' : host}
    return render(request,'posts/makepost.html',context)

def postdetails(request: HttpRequest, post_id):
    if request.user.is_anonymous:
        return render(request,'core/index.html')
    currentAuthor=Author.objects.filter(userId=request.user).first()
    host = Utils.getRequestHost(request)
    post_id = Utils.cleanPostId(post_id, host)

    target_host = Utils.getUrlHost(post_id)
    if (not target_host or Utils.areSameHost(target_host, host)):
        target_host = host

    comments = None
    postLikes= None
    num_post_likes = None
    posts = None
    if target_host == host:
        posts = Post.objects.filter(id=post_id)
        for i in posts:
            comments = get_comments(i.id)
            postLikes= get_likes_post(i.id)
            num_post_likes = len(postLikes)
    else:
        posts = Utils.getFromUrl(post_id)
        if (posts.__contains__("data")):
            posts = posts["data"]

    template = loader.get_template('posts/postdetails.html')
    context = {
        'posts': posts,
        'comments': comments,
        'num_post_likes': num_post_likes,
        }
    return render(request, 'posts/postdetails.html', context)


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
def get_comments_lmtd(post_id):
    comments = Comment.objects.filter(post=post_id)[:3]
    return comments

def get_comments(post_id):
    comments = Comment.objects.filter(post=post_id)
    return comments

def get_likes_post(post_id):
    likes = Like.objects.filter(post=post_id)
    return likes

def get_likes_comments(comment_id):
    likes = Like.objects.filter(comment= comment_id)
