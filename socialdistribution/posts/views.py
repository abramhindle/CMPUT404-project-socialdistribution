from datetime import datetime

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.db import models

from .models import Post, Comment
from .forms import PostForm, CommentForm
from profiles.models import Author
from django.contrib.auth.decorators import login_required


@login_required(login_url = "login")
def index(request):

    template = 'posts/posts_base.html'
    latest_post_list = Post.objects.order_by('-published')[:5]
    author = request.user
    context = {
        'latest_post_list': latest_post_list,
        'author': author,
    }

    return render(request, template, context)


def postDetails(request, post_id):
    return HttpResponse("You are looking at post %s. " % post_id)


def post_comments(request, post_id):
    return HttpResponse("You are looking at the comments of post %s. " % post_id)


def view_post(request, post_id):
    template = 'posts/posts_view.html'
    post = Post.objects.get(id=post_id)

    latest_post_list = Post.objects.order_by('-published')[:5]
    author = request.user

    comments = Comment.objects.filter(post=post).order_by('published')

    if request.method == 'POST':
        comment_form = CommentForm(request.POST or None)
        if comment_form.is_valid():
            content = request.POST.get('comment')
            author = Author.objects.get(email= 'um4r12@gmail.com')  # hardcode here -TODO
            comment = Comment.objects.create(post=post, author=author, comment=content)
            comment.save()
            return HttpResponseRedirect(request.path_info)
        # What should we do if the form is invalid?
    else:
        comment_form = CommentForm()

    context = {
        'latest_post_list': latest_post_list,
        'author': author,
        'post': post,
        'comments': comments,
        'comment_form': comment_form,
    }

    return render(request, template, context)
