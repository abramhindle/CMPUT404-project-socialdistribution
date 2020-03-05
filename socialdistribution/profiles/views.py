from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

from .models import Author
from posts.forms import PostForm
from .forms import ProfileForm

# Create your views here.


def index(request):
    author = Author.objects.get(displayName='cc')   #hardcode here

    context = {
        'author': author,
    }

    return render(request, 'profiles/index_base.html', context)


def new_post(request):
    form = PostForm()
    author = Author.objects.get(displayName='cc')

    context = {
        'form': form,
        'author': author,
    }

    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            form.save()
            url = reverse('index')
            return HttpResponseRedirect(url)

    return render(request, 'posts/posts_form.html', context)

def post_image(request):
    form = PostForm()
    author = Author.objects.get(displayName='cc')

    context = {
        'form': form,
        'author': author,
    }

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            url = reverse('index')
            return HttpResponseRedirect(url)

    return render(request, 'posts/post_image.html', context)

def current_visible_posts(request):
    return HttpResponse("Only these posts are visible to you: ")


def author_posts(request, author_id):
    return HttpResponse("Here are the posts of %s: ", author_id)

def view_profile(request):
    author = Author.objects.get(displayName= 'cc')
    form = ProfileForm(instance=author)

    context = {
        'form': form,
        'author': author,
    }
    return render(request, 'profiles/profiles_view.html', context)


def edit_profile(request):
    author = Author.objects.get(displayName='cc')   #hardcode here
    form = ProfileForm(request.POST or None, instance=author)

    context = {
        'form': form,
        'author': author,
    }

    if request.method == 'POST':

        if form.is_valid():
            form.save()
            url = reverse('editprofile')
            return HttpResponseRedirect(url)

    return render(request, 'profiles/profiles_edit.html', context)
