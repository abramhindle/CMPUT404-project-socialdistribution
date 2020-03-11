from django.http import HttpResponse, HttpResponsePermanentRedirect
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
import pdb


def paginated_result(objects, request, keyword, **result):
    page_num = int(request.GET.get('page', 0))
    size = int(request.GET.get('size', 10))
    first_result = size*page_num
    count = objects.count()
    if count <= first_result:
        first_result = 0
        page_num = 0
        # JUST SETS TO PAGE 0, we could : Redirect to page 0? 400 Bad Request?
    last_result = first_result + size

    result["count"] = count
    result["size"] = size
    result["previous"] = page_num - 1 if page_num >= 1 else None
    result["next"] = page_num + 1 if objects.count() >= last_result else None
    result[keyword] = objects[first_result:last_result]
    return result


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
            print("SAVED")
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

# https://stackoverflow.com/questions/18284010/django-modelform-not-saving-data-to-database


def new_post(request):
    if request.method == "POST":
        print(request.POST)
        data = request.POST.copy()
        data['author'] = Author.objects.get(username=request.user)
        print(data)
        form = NewPostForm(data)
        if form.is_valid():
            print("VALID")
            # form.save(commit=False)
            # form.author = Author.objects.get(username=request.user)
            form.save()
            return redirect('explore')
        else:
            form = NewPostForm()
            return render(request, 'sd/new_post.html', {'form': form})
    else:
        form = NewPostForm()
        return render(request, 'sd/new_post.html', {'form': form})

    page = 'sd/new_post.html'
    return render(request, page)


def account(request):
    page = 'sd/account.html'
    return render(request, page)


def search(request):
    page = 'sd/search.html'
    return render(request, page)


def notifications(request):
    page = 'sd/notifications.html'
    return render(request, page)


def requests(request):
    return HttpResponse("Friend Requests Page")


def feed(request):
    all_posts = Post.objects.all()
    result = paginated_result(all_posts, request, "feed", query="feed")
    page = 'sd/feed.html'
    return render(request, page, result)


def explore(request):
    all_posts = Post.objects.all()
    result = paginated_result(all_posts, request, "feed", query="feed")
    return render(request, 'sd/index.html', result)


def author(request, author_id):
    try:
        author = Author.objects.get(uuid=author_id)
    except:
        raise Exception(404)
    return HttpResponse(author.username+"'s Page")


def post(request, post_id):
    try:
        post = Post.objects.get(uuid=post_id)
    except:
        raise Exception(404)
    result = {
        "query": "post",
        "title": post.title,
        # "source" : post.source,
        # "description" : post.description,
        # "contentType" : post.contentType,
        "content": post.body,
        "author": {
            "host": post.author.host,
            "id":  post.author.uuid,
            "url": post.author.uuid,  # we need a URL
            "displayName": post.author.username,  # display name???
            "github": post.author.github
        },
        # "categories" : post.categories,
        # are we implementing comments inside post?
        "published": post.date,
        "id": post.uuid,
        "visibleTo": post.viewable_to
    }
    return HttpResponse("Post Page")
    return render(request, 'sd/index.html', result)  # posts page


def post_comment(request, post_id):
    comments = Comment.objects.filter(post=post_id)
    result = paginated_result(comments, request, "comments", query="comments")
    return HttpResponse("Post Comments Page")
    return render(request, 'sd/index.html', result)  # post commments page


def friends(request):
    return HttpResponse("Friends Page")


