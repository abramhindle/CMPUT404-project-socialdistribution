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
from django.contrib.auth import get_user_model
from .forms import *
import os
import pdb


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


class AuthorLoginAPIView(APIView):
    pass
#     permission_classes = [AllowAny]
#     serializer_class = LoginAuthorSerializer

#     def post(self, request, format=None):
#         print(request.data)
#         serializer = self.serializer_class(data=request.data)
#         print(serializer)
#         serializer.is_valid()
#         print("VALID")
#         print(serializer.validated_data)
#         username = serializer.validated_data['username']
#         token = Token.objects.get(username=username)
#         print("WORKS?")
#         return Response(
#             status=status.HTTP_200_OK,

#         )


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

    # Creates Post by sending (example):
    # {
    #   "title": "ExampleTitle",
    #   "body": "ExampleBody",
    #   "status": "pub",
    #   "link_to_image": "https://github.com/UAlberta-CMPUT401/ResuscitationSim/blob/master/backend/haptik/views.py",
    #   "author": "0248f053-b2a7-433a-a970-dffa58b66b91",
    #   "uuid": "714b1e76-da65-445f-91f8-4f54da332e3d"
    # }
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        print(serializer)
        serializer.is_valid(raise_exception=True)
        print("VALID")
        self.perform_create(serializer)
        print("perform created")

        # post_uuid = Post.objects.latest('date')
        post_uuid = {'uuid': Post.objects.latest('date').uuid}

        headers = self.get_success_headers(serializer.data)
        return Response(
            {**serializer.data, **post_uuid},
            status=status.HTTP_201_CREATED,
            headers=headers
        )


class GetPostAPIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = GetPostSerializer

    # Returns Post by sending UUID of Post
    # {"uuid":"7feecf20-5694-4ff0-afd1-bade95228fb3" }
    def get(self, request, format=None):
        post = Post.objects.get(uuid=request.data['uuid'])
        serializer = GetPostSerializer(post)

        return Response(serializer.data, status=status.HTTP_200_OK)


class GetAllAuthorPostAPIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = GetPostSerializer

    # Returns All Author's Posts by sending UUID of Author
    def get(self, request, format=None):
        posts = Post.objects.filter(author=request.data['uuid'])
        serializer = GetPostSerializer(posts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class DeletePostAPIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = DeletePostSerializer

    def get(self, request, format=None):
        token = request.META["HTTP_AUTHORIZATION"]
        token = token.split()[1]
        token_author_uuid = Author.objects.get(auth_token=token).uuid
        post_author_uuid = Post.objects.get(
            uuid=request.data['uuid']).author.uuid

        print(token_author_uuid)
        print(post_author_uuid)

        if token_author_uuid == post_author_uuid:
            Post.objects.get(uuid=request.data['uuid']).delete()
            return Response(status=status.HTTP_200_OK)
        else:
            print("INEQUAL")
            return Response(status=status.HTTP_401_UNAUTHORIZED)


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


def requests(request):
    return HttpResponse("Friend Requests Page")


def feed(request):
    return HttpResponse("Your Feed")


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

# def search(request):
# 	return HttpResponse("User Search Page")


def account(request):
    return HttpResponse("Your Account Page")
