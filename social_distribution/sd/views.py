from django.http import HttpResponse, HttpResponsePermanentRedirect
from django.shortcuts import render, redirect
from rest_framework.generics import CreateAPIView, RetrieveAPIView
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.contrib.auth.hashers import check_password
from .models import *
from .serializers import *
from django.utils import timezone
from rest_framework.parsers import JSONParser
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.models import User
from .forms import *
import os, pdb, json, uuid

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
    result[keyword] = list(objects[first_result:last_result])
    return result


User = get_user_model()


def index(request):
    all_posts = Post.objects.all()
    result = paginated_result(all_posts, request, "feed", query="feed")
    user = get_current_user(request)
    return render(request, 'sd/index.html', {"result": result, "current_user": user})


def explore(request):
    all_posts = Post.objects.all()
    result = paginated_result(all_posts, request, "feed", query="feed")
    return render(request, 'sd/index.html', {'current_user': None, 'authenticated': False, 'result': result})


def account(request):
    if authenticated(request):
        user = get_current_user(request)
        page = 'sd/account.html'
        return render(request, page, {'current_user': user, 'authenticated': True})
    else:
        return redirect('login')


def search(request):
    page = 'sd/search.html'
    return render(request, page)


def notifications(request):
    page = 'sd/notifications.html'
    return render(request, page)


def post_comment(request, post_id):
    comments = Comment.objects.filter(post=post_id)
    result = paginated_result(comments, request, "comments", query="comments")
    return HttpResponse("Post Comments Page")
    return render(request, 'sd/index.html', result)  # post commments page


def authenticated(request):
    try:
        if(request.session['authenticated']):
            return True
    except KeyError as k:
        print("request.session['authenticated'] not set")
        return False


def get_current_user(request):
    if authenticated(request):
        uid = request.session['auth-user']
        new_id = uuid.UUID(uid)
        author = Author.objects.get(uuid=new_id)
        return author
    else:
        return None


def login(request):
    if request.method == "GET":
        return render(request, 'sd/login.html', {'current_user': None, 'authenticated': False})

    info = request._post
    user_name = info['username']
    pass_word = info['password']
    try:
        user = Author.objects.get(username=user_name)
    except:
        request.session['authenticated'] = False
        return redirect('login')

    if (pass_word != user.password) and not (check_password(pass_word, user.password)):
        return redirect('login')

    request.session['authenticated'] = True
    key = Author.objects.get(username=user_name).uuid
    request.session['auth-user'] = str(key)
    request.session['SESSION_EXPIRE_AT_BROWSER_CLOSE'] = True
    return redirect('my_feed')

def register(request):
    if request.method == "GET":
        return render(request, 'sd/register.html', {'current_user': None, 'authenticated': False})

    info = request._post
    serializer = CreateAuthorSerializer(data=info)
    if serializer.is_valid():
        serializer.save()
        request.session['authenticated'] = True
        user = Author.objects.get(username=serializer.data['username'])
        key = user.uuid
        request.session['auth-user'] = str(key)
        request.session['SESSION_EXPIRE_AT_BROWSER_CLOSE'] = True
        return render(request, 'sd/index.html', {'current_user': user, 'authenticated': True})
    else:
        return render(request, 'sd/register.html', {'current_user': None, 'authenticated': False} )

def logout(request):
    try:
        request.session['authenticated'] = False
        request.session.pop('auth-user')
        request.session.flush()
    except KeyError as k:
        print("Not currently authenticated, returning to feed")
    return redirect('explore')


def new_post(request):
    if not authenticated(request):
        return redirect('login')

    user = get_current_user(request)
    if request.method == "GET":
        form = NewPostForm()
        return render(request, 'sd/new_post.html', {'form': form, 'current_user': user, 'authenticated': True})

    else:
        info = dict(request._post)
        for i in info:
            if isinstance(info[i],list):
                info[i] = info[i][0]
        info['author'] = user.uuid
        serializer = CreatePostSerializer(data=info)
        if serializer.is_valid():
            serializer.save()
            page = 'sd/feed.html'
            print('POST SUCCESSFUL')
            return redirect('my_feed')
        else:
            form = NewPostForm()
            print('POST FAILED, PLEASE TRY AGAIN')
            return render(request, 'sd/new_post.html', {'form': form, 'current_user': user, 'authenticated': True})


def feed(request):
    if authenticated(request):
        print("VERIFIED LOGIN")
        user = get_current_user(request)
        print(user.username+" IS LOGGED IN")
        page = 'sd/feed.html'
        return render(request, page, {'current_user': user, 'authenticated': True})
    else:
        print("NOT LOGGED IN")
        page = 'sd/index.html'
        return render(requests, page, {'current_user': None, 'authenticated': False})
