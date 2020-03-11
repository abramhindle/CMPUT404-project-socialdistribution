from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.template.defaulttags import csrf_token
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from .decorators import check_authentication

# from django.contrib.auth.form import UserCreationForm
from django.contrib import messages

from .models import Author
from posts.forms import PostForm
from .forms import ProfileForm, ProfileSignup
from django.shortcuts import render, redirect
# import logging
from django.conf import settings

# Create your views here.


def get_user_id(request):
    user_id = str(request.user.id).replace("-","")
    return user_id


def login(request):
    return render(request, 'login.html', {'form': form})
    # return render(request, 'login/login.html', {})


def index(request):
    author = request.user

    context = {
        'author': author,
    }

    return render(request, 'profiles/index_base.html', context)


def new_post(request):
    form = PostForm()
    author = request.user

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

    return render(request, 'posts/posts_form.html', context)


def current_visible_posts(request):
    return HttpResponse("Only these posts are visible to you: ")


def author_posts(request, author_id):
    return HttpResponse("Here are the posts of %s: ", author_id)


def view_profile(request):
    context = {}
    if request.user.is_authenticated:
        author = request.user
        form = ProfileForm(instance=author)
        context['author'] = author

        return render(request, 'profiles/profiles_view.html', context)
    else:
        return render(request, '404.html', context)


@check_authentication
def edit_profile(request):

    author = request.user
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


def register(request):
    if request.method == "POST":
        form = ProfileSignup(request.POST)
        print("BEFORE")
        if form.is_valid():
            print("FORM VALID")
            form.save()
            return redirect("accounts/login")
        return redirect("/stream/")
    else:
        form = ProfileSignup()
    return render(request, "login/register.html", {"form": form})
