from django.shortcuts import render, redirect, get_object_or_404
from django.http.request import HttpRequest

from apis.posts.views import post
from .models import Post
from .models import Like
from .models import Comment
from apps.core.models import Author
from socialdistribution.utils import Utils

def index(request: HttpRequest):
    # should include friends etc at some points
    posts = Post.objects.filter(unlisted=False, visibility="PUBLIC")

    for post in posts:
        post.comments_top3 = get_3latest_comments(post.id)
        post.num_likes = len(get_likes_post(post.id))

    host = request.scheme + "://" + request.get_host()
    context = {
        'posts': posts,
        'host': host,
        }
    return render(request, 'posts/index.html', context)

def my_posts(request: HttpRequest):
    if request.user.is_anonymous or not (request.user.is_authenticated):
        return render(request,'posts/index.html')

    currentAuthor = Author.objects.get(userId=request.user)
    posts = Post.objects.filter(author=currentAuthor)
    for post in posts:
        post.comments_top3 = get_3latest_comments(post.id)
        post.num_likes = len(get_likes_post(post.id))

    host = request.scheme + "://" + request.get_host()
    context = {
        'posts': posts,
        'host': host,
        'userAuthor': currentAuthor
        }
    return render(request, 'posts/index.html', context)

def makepost(request: HttpRequest):
    if request.user.is_anonymous or not (request.user.is_authenticated):
        return render(request,'posts/makepost.html')

    currentAuthor = Author.objects.filter(userId=request.user).first()
    host = request.scheme + "://" + request.get_host()
    context = {'author' : currentAuthor, 'host' : host}
    return render(request,'posts/makepost.html',context)

def postdetails(request: HttpRequest, post_id):
    if request.user.is_anonymous:
        return render(request,'core/index.html')

    currentAuthor = Author.objects.get(userId=request.user)
    host = Utils.getRequestHost(request)
    post_id = Utils.cleanPostId(post_id, host)
    target_host = Utils.getUrlHost(post_id)
    if (not target_host or Utils.areSameHost(target_host, host)):
        target_host = host

    if target_host == host:
        post = get_object_or_404(Post, id=post_id)
        post.page_comments = get_comments(post.id)
        post.num_likes = len(get_likes_post(post.id))
    else:
        post_resp = Utils.getFromUrl(post_id)
        if (post_resp.__contains__("data")):
            post = post_resp["data"]
            # TODO This probably needs more for the foreign host

    context = {
        'post': post,
        'host': host,
        'userAuthor': currentAuthor,
        # TODO correct page size based on pagination
        'page_size': 10
        }
    return render(request, 'posts/postdetails.html', context)


def editpost(request: HttpRequest, post_id: str):
    if request.user.is_anonymous or not (request.user.is_authenticated):
        return render(request,'posts/editpost.html')

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

def get_3latest_comments(post_id):
    comments = Comment.objects.filter(post=post_id)[:3]
    return comments

def get_comments(post_id):
    comments = Comment.objects.filter(post=post_id)
    return comments

def get_likes_post(post_id):
    likes = Like.objects.filter(post=post_id)
    return likes
