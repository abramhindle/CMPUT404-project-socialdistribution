from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from posts.forms import PostForm
from django.urls import reverse

# Create your views here.


def index(request):
    return render(request, 'profiles/index_base.html', {})

def author_profile(request):
    form = PostForm()

    context = {
        'form': form,
    }

    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            form.save()
            url = reverse('index')
            return HttpResponseRedirect(url)

    return render(request, 'posts/posts_form.html', context) 

def current_visible_posts(request):
    return HttpResponse("Only these posts are visible to you: ")

def author_posts(request, author_id):
    return HttpResponse("Here are the posts of %s: ", author_id)

