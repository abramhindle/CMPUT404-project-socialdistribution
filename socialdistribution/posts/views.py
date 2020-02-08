from django.shortcuts import render
from django.http import HttpResponse

from .models import PostId
from .forms import PostForm

def index(request):
    template = 'posts/posts_base.html'
    latest_post_list = PostId.objects.order_by('-pub_date')[:5]
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