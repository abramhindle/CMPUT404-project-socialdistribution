from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.template.defaulttags import csrf_token
# from django.contrib.auth.form import UserCreationForm
from django.contrib import messages

from .models import Author
from posts.forms import PostForm
from .forms import ProfileForm, ProfileSignup
from django.shortcuts import render, redirect
import logging
from django.conf import settings

# Create your views here.

def login(request):
    return render(request, 'login.html', {'form': form})
    # return render(request, 'login/login.html', {})


def registerss(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST)
        if form.is_valid():
            logging.debug("FORM IS VALID")
            user = form.save()
            user.refresh_from_db()  # load the profile instance created by the signal
            user.save()
            
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            return redirect('/posts')
        logging.debug("NOT VALID")
    else:
        logging.debug("DIDNT WORK")
        form = ProfileForm()
    return render(request, 'registration.html', {'form': form})

def index(request):
    author = Author.objects.get(displayName='Xiaole')   #hardcode here

    context = {
        'author': author,
    }

    return render(request, 'profiles/index_base.html', context)

def new_post(request):
    form = PostForm()
    author = Author.objects.get(displayName='Xiaole')


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
    author = Author.objects.get(displayName= 'Xiaole')
    form = ProfileForm(instance=author)

    context = {
        'form': form,
        'author': author,
    }
    return render(request, 'profiles/profiles_view.html', context)


def edit_profile(request):
    author = Author.objects.get(displayName='Xiaole')   #hardcode here
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
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            message.success(request, f'Account created for {username}!')
            return redirect('login')
        #If get here, means taht form isn't valid
        print(form )
        return redirect('posts')
    else:
        form = ProfileForm()
    return render(request, 'login/register.html', {'form':form})