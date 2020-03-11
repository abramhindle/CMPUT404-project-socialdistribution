from django.http import HttpResponse, HttpResponsePermanentRedirect
from django.shortcuts import render, redirect
from rest_framework.generics import CreateAPIView, RetrieveAPIView
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .models import *
from .serializers import *
from django.utils import timezone
from rest_framework.parsers import JSONParser
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.models import User
from .forms import *
import os
import pdb
import json


class CreateAuthorAPIView(CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = CreateAuthorSerializer

    def create(self, request, *args, **kwargs):
        print(request.data)
        serializer = self.get_serializer(data=request.data)
        # print(serializer)
        serializer.is_valid(raise_exception=True)
        print("VALID")
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        token = Token.objects.create(user=serializer.instance)
        token_data = {"token": token.key}
        return Response(
            {**serializer.data, **token_data},
            status=status.HTTP_201_CREATED,
            headers=headers
        )


class AuthorLogoutAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, format=None):
        print(request.user)
        request.user.auth_token.delete()
        return Response(
            status=status.HTTP_200_OK
        )


class GetAuthorAPIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = GetAuthorSerializer

    def get(self, request, format=None):
        token = request.META["HTTP_AUTHORIZATION"]
        token = token.split()[1]
        author = Author.objects.get(auth_token=token)
        serializer = GetAuthorSerializer(author)
        print(serializer.data)

        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )


class CreatePostAPIView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CreatePostSerializer

    def create(self, request, *args, **kwargs):
        token = request.META["HTTP_AUTHORIZATION"]
        token = token.split()[1]
        print("TOKEN: ", token)
        author = Author.objects.get(auth_token=token)
        print(request.data)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        headers = self.get_success_headers(serializer.data)
        return Response(
            {**serializer},
            status=status.HTTP_201_CREATED,
            headers=headers

        )


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
    print(result)
    return render(request, 'sd/index.html', result)
    # return redirect('explore', permanent=True)

def explore(request):
    all_posts = Post.objects.all()
    result = paginated_result(all_posts, request, "feed", query="feed")
    return result

def posts_api_json(request):
    all_posts = Post.objects.all()
    result = paginated_result(all_posts, request, "posts", query="posts")
    print(json.dumps(result))
    return HttpResponse(json.dumps(result))


def login(request):

    if request.method == "GET":
        return render(request, 'sd/login.html')
    pdb.set_trace()
    u = str(request._post['username'])
    p = str(request._post['password'])
    try:
        user = Author.objects.get(username=username)
    except:
        return redirect('login' ,{'invalid_login':True})

    if password != user.password:
        return redirect('login' ,{'invalid_login':True})

    token = Token.objects.get(user=user.uuid)
    response = Response()
    # pdb.set_trace()
    # if Tokens.objects.filter(key=token)
        
    return render(request, "sd/index.html")


# def logout(request):
#     return HttpResponse("Logout Page")

# Sources:
# https://www.youtube.com/watch?v=q4jPR-M0TAQ&list=PL-osiE80TeTtoQCKZ03TU5fNfx2UY6U4p&index=6

# def register(request):
#     if request.method == "POST":
#         form = RegistrationForm(request.POST)
#         if form.is_valid():
#             form.save()
#             print("SAVED")
#             username = form.cleaned_data.get('username')
#             messages.success(request, f'Account created for {username}!')
#             # return render(request, 'sd/index.html', {'message': messages})
#             return redirect('login')
#         else:
#             form = RegistrationForm()
#             messages.error(
#                 request, f'Invalid characters used! Please try again')
#             return render(request, 'sd/register.html', {'form': form})

#     else:
#         form = RegistrationForm()
#         return render(request, 'sd/register.html', {'form': form})

def register(request):
    print("REGISTER")
    print(request.method)
    if request.method == "POST":
        print(request.POST)
        data = request.POST.copy()

        serializer = CreateAuthorSerializer(data=request.POST)
        print(serializer)
        if serializer.is_valid():
            serializer.save()
            return render(request, 'sd/index.html')
        else:
            return render(request, 'sd/register.html')

    else:
        print("GET")
        return render(request, 'sd/register.html')


def create_account(request):
    page = 'sd/create_account.html'
    return render(request, page)

# https://stackoverflow.com/questions/18284010/django-modelform-not-saving-data-to-database


def new_post(request):
    token = request.headers['Cookie'].split('=')[1]
    if not Token.objects.filter(key=token):
        return redirect('login')

    if request.method == "POST":
        print(request.POST)
        data = request.POST.copy()
        pdb.set_trace()
        data['author'] = Author.objects.get(auth_token=token)
        print(data)
        form = NewPostForm(data)
        if form.is_valid():
            print("VALID")
            # form.save(commit=False)
            pdb.set_trace()
            form.author = Author.objects.get(username=request.user)
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


def requests(request):
    return HttpResponse("Friend Requests Page")


def feed(request):
    return HttpResponse("Your Feed")



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

# def search(request):
# 	return HttpResponse("User Search Page")


def account(request):
    return HttpResponse("Your Account Page")
