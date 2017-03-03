from django.shortcuts import render
from django.http import Http404
from . models import Post

def index(request):
    all_posts = Post.objects.all()
    context = {
        'all_posts': all_posts,
    }

    return render(request, 'post/index.html', context)

def detail(request, post_id):
    try:
        post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        raise Http404("Post does not exist")

    return render(request, 'post/detail.html', {'post': post})

