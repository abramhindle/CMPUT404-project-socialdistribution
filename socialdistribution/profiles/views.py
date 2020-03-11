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

from .utils import getFriendsOfAuthor, getFriendRequestsToAuthor,\
                   getFriendRequestsFromAuthor
from django.views.decorators.csrf import csrf_exempt
import base64

# Create your views here.

def get_user_id(request):
    user_id = str(request.user.id).replace("-","")
    print(user_id)
    return user_id

def login(request):
    return render(request, 'login.html', {'form': form})
    # return render(request, 'login/login.html', {})

def index(request):
    # This a view that display the navigation of the author. 
    # In the navigation, author can view/edit it's profile and dashboard.
    # Author can choose their actions such as look at the friends page,
    # post a new post, etc.
    # TODO: remove hardcode
    template = 'profiles/index_base.html'

    author = Author.objects.get(id = get_user_id(request))   #test check if good

    context = {
        'author': author,
    }

    return render(request, template, context)

@csrf_exempt
def new_post(request):

    # TODO: remove hardcode
    template = 'posts/posts_form.html'

    form = PostForm()
    author = Author.objects.get(id = get_user_id(request))

    context = {
        'form': form,
        'author': author,
    }

    if request.method == 'POST':
        form = PostForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            new_content = form.save(commit=False)
            cont_type = form.cleaned_data['content_type']
            if(cont_type == "image/png;base64" or cont_type == "image/jpeg;base64" ):
                img = form.cleaned_data['image_file']
                new_content.content = (base64.b64encode(img.file.read())).decode("utf-8")

            new_content.save()
            url = reverse('index')
            return HttpResponseRedirect(url)

    return render(request, template, context)


def current_visible_posts(request):
    return HttpResponse("Only these posts are visible to you: ")


def author_posts(request, author_id):
    return HttpResponse("Here are the posts of %s: ", author_id)


def view_profile(request):
    template = 'profiles/profiles_view.html'
    
    # TODO: remove hardcode
    author = Author.objects.get(id = get_user_id(request)) #check if good
    form = ProfileForm(instance=author)

    context = {
        'author': author,
    }
    return render(request, template, context)

@check_authentication
def edit_profile(request):
    template = 'profiles/profiles_edit.html'
  
    # TODO: remove hardcode
    # author = Author.objects.get(displayName='Xiaole')   #hardcode here
    author = Author.objects.get(id=get_user_id(request))  
    form = ProfileForm(request.POST or None, request.FILES or None, instance=author)
    context = {
        'form': form,
        'author': author,
    }

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            url = reverse('editprofile')
            return HttpResponseRedirect(url)
    
    return render(request, template, context)


def register(request):
    if request.method == "POST":
        form = ProfileSignup(request.POST)
        print("BEFORE")
        if form.is_valid():
            print("FORM VALID")
            form.save()
            print("USER SAVED")
            return redirect("/accounts/login")
        return redirect("/register")
    else:
        form = ProfileSignup()
    return render(request, "login/register.html", {"form":form})


def my_friends(request):
    # TODO: remove hardcode
    template = 'friends/friends_list.html'

    author = Author.objects.get(id = get_user_id(request))   #check if good
    friendList = getFriendsOfAuthor(author)

    context = {
        'author': author,
        'friendList': friendList,
    }
    return render(request, template, context)


def my_friend_requests(request):
    # TODO: remove hardcode
    template = 'friends/friends_request.html'

    author = Author.objects.get(id = get_user_id(request))   #check if goof
    friendRequestList = getFriendRequestsToAuthor(author)


    context = {
        'author': author,
        'friendRequestList': friendRequestList,
    }
    return render(request, template, context)


def my_friend_following(request):
    # TODO: remove hardcode
    template = 'friends/friends_follow.html'

    author = Author.objects.get(id = get_user_id(request))   #check if good
    friendFollowList = getFriendRequestsFromAuthor(author)

    context = {
        'author': author,
        'friendFollowList': friendFollowList,
    }

    return render(request, template, context)
