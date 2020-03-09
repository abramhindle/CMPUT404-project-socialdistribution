from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import *
from .serializers import *
from django.utils import timezone
from rest_framework.parsers import JSONParser
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import get_user_model
from .forms import *
import os

User = get_user_model()


def index(request):
    return redirect('explore', permanent=True)


# def login(request):
#     if request.method == "POST":
#         form = LoginForm(request.POST)
#         if form.is_valid():

#     return HttpResponse("Login Page")


# def logout(request):
#     return HttpResponse("Logout Page")

# Sources:
# https://www.youtube.com/watch?v=q4jPR-M0TAQ&list=PL-osiE80TeTtoQCKZ03TU5fNfx2UY6U4p&index=6

def register(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            # return render(request, 'sd/index.html', {'message': messages})
            return redirect('login')
        else:
            form = RegistrationForm()
            messages.error(
                request, f'Invalid characters used! Please try again')
            return render(request, 'sd/register.html', {'form': form})

    else:
        form = RegistrationForm()
        return render(request, 'sd/register.html', {'form': form})


def create_account(request):
    page = 'sd/create_account.html'
    return render(request, page)


def new_post(request):
    page = 'sd/new_post.html'
    return render(request, page)


def account(request):
    page = 'sd/account.html'
    return render(request, page)


def requests(request):
    return HttpResponse("Friend Requests Page")


def feed(request):
    return HttpResponse("Your Feed")


def explore(request):
    feed = Post.objects.all()
    page = 'sd/index.html'
    return render(request, page, {'feed': feed})


def author(request, author_id):
    author = Author.objects.get(uuid=author_id)
    return HttpResponse(author.username+"'s Page")


def post(request, post_id):
    post = Post.objects.get(uuid=post_id)
    return HttpResponse(post)


def post_comment(request, post_id):
    post = Comment.objects.get(post=post_id)
    return HttpResponse(post)

# def search(request):
# 	return HttpResponse("User Search Page")

# def friends(request):
# 	return HttpResponse("Friends Page")

# def account(request):
# 	return HttpResponse("Your Account Page")
