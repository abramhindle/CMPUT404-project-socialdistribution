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


def postsDetail(request, post_id):
    return HttpResponse("You are looking at post %s. " % post_id)


def view_post(request):
    template = 'posts/view_post.html'
    form = PostForm(request.Get or None)

    context = {
        'form': form,
    }

    return render(request, template, context)
