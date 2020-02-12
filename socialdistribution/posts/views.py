from django.shortcuts import render
from django.http import HttpResponse

from .models import Post
from .forms import PostForm


def index(request):
    template = 'posts/posts_base.html'
    latest_post_list = Post.objects.order_by('-published')[:5]
    context = {
        'latest_post_list': latest_post_list,
    }

    return render(request, template, context)


def postDetails(request, post_id):
    return HttpResponse("You are looking at post %s. " % post_id)

def postComments(request, post_id):
    return HttpResponse("You are looking at the comments of post %s. " % post_id)

def view_post(request, post_id):
    template = 'posts/posts_view.html'
    post = Post.objects.get(id=post_id)

    context = {
        'post': post,
    }

    return render(request, template, context)
