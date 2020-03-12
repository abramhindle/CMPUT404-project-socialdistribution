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
import uuid


class CreateAuthorAPIView(CreateAPIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
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
        print(request.user)
        print(request.auth)

        return Response(
            {**serializer.data},
            status=status.HTTP_201_CREATED,
            headers=headers
        )


class AuthorLoginAPIView(CreateAPIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        print(request.data)
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        print("VALID")
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
        })


class AuthorLogoutAPIView(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        print(request.user)
        request.user.auth_token.delete()
        return Response(
            status=status.HTTP_200_OK
        )


class AuthorUpdateAPIView(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    serializer = AuthorSerializer

    def put(self, request, pk, format=None):
        author = Author.objects.get(pk=pk)
        serializer = AuthorSerializer(
            instance=author, data=request.data, partial=True)

        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


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
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    # permission_classes = [IsAuthenticated]
    serializer_class = AuthorSerializer

    def get(self, request, pk, format=None):
        author = Author.objects.get(uuid=pk)
        serializer = AuthorSerializer(author)
        print(serializer.data)

        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )


class CreatePostAPIView(CreateAPIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    # permission_classes = [IsAuthenticated]
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
    def create(self, request, pk):
        data = request.data.copy()
        data['author'] = pk
        serializer = self.get_serializer(data=data)
        print(serializer)
        serializer.is_valid(raise_exception=True)
        print("VALID")
        self.perform_create(serializer)
        print("perform created")

        headers = self.get_success_headers(serializer.data)
        return Response(
            {**serializer.data},
            status=status.HTTP_201_CREATED,
            headers=headers
        )


class GetPostAPIView(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    # permission_classes = [IsAuthenticated]
    serializer_class = GetPostSerializer

    # Returns Post by sending UUID of Post
    def get(self, request, pk, format=None):
        post = Post.objects.get(uuid=pk)
        serializer = GetPostSerializer(post)

        return Response(serializer.data, status=status.HTTP_200_OK)


class GetAllAuthorPostAPIView(APIView):
    authentication_classes = [BasicAuthentication, SessionAuthentication]
    serializer_class = GetPostSerializer

    # Returns All Author's Posts by sending UUID of Author
    def get(self, request, pk, format=None):
        posts = Post.objects.filter(author=pk)
        posts = posts.filter(status='pub')
        serializer = GetPostSerializer(posts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class GetAllVisiblePostAPIView(APIView):
    serializer_class = GetPostSerializer

    def get(self, request, format=None):
        posts = Post.objects.filter(status='pub')
        serializer = GetPostSerializer(posts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class DeletePostAPIView(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = DeletePostSerializer

    # def get(self, request, format=None):
    #     token = request.META["HTTP_AUTHORIZATION"]
    #     token = token.split()[1]
    #     token_author_uuid = Author.objects.get(auth_token=token).uuid
    #     post_author_uuid = Post.objects.get(
    #         uuid=request.data['uuid']).author.uuid

    #     print(token_author_uuid)
    #     print(post_author_uuid)

    #     if token_author_uuid == post_author_uuid:
    #         Post.objects.get(uuid=request.data['uuid']).delete()
    #         return Response(status=status.HTTP_200_OK)
    #     else:
    #         print("INEQUAL")
    #         return Response(status=status.HTTP_401_UNAUTHORIZED)


class CreateCommentAPIView(CreateAPIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    serializer_class = CreateCommentSerializer

    def create(self, request, pk):
        print(pk)
        data = request.data.copy()
        data['post'] = pk
        print(data)
        serializer = self.get_serializer(data=data)
        # print(serializer)
        serializer.is_valid(raise_exception=True)
        # print("VALID")
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        return Response(
            {**serializer.data},
            status=status.HTTP_201_CREATED,
            headers=headers
        )


class GetPostCommentsAPIView(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    # permission_classes = [IsAuthenticated]
    serializer_class = CommentSerializer

    def get(self, request, pk):
        comments = Comment.objects.filter(post=pk)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CreateFriendRequestAPIView(CreateAPIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    serializer_class = FriendRequestSerializer

    def create(self, request):
        data = request.data
        print(data)
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        return Response(
            {**serializer.data},
            status=status.HTTP_201_CREATED,
            headers=headers
        )


class GetAllAuthorFriendRequest(APIView):
    serializer_class = FriendRequestSerializer

    def get(self, request, pk):
        friend_requests = FriendRequest.objects.filter(to_author=pk)
        serializer = FriendRequestSerializer(friend_requests, many=True)
        return Response(
            serializer.data, status=status.HTTP_200_OK
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
    # print(result)
    return render(request, 'sd/index.html', result)
    # return redirect('explore', permanent=True)


def explore(request):
    all_posts = Post.objects.all()
    result = paginated_result(all_posts, request, "feed", query="feed")
    return render(request, 'sd/index.html', result)


def posts_api_json(request):
    all_posts = Post.objects.all()
    result = paginated_result(all_posts, request, "posts", query="posts")
    # print(json.dumps(result))
    return HttpResponse(json.dumps(result))


def register(request):
    # print("REGISTER")
    # print(request.method)
    if request.method == "POST":
        # print(request.POST)
        data = request.POST.copy()

        serializer = CreateAuthorSerializer(data=request.POST)
        # print(serializer)
        if serializer.is_valid():
            serializer.save()
            return render(request, 'sd/index.html')
        else:
            return render(request, 'sd/register.html')

    else:
        # print("GET")
        return render(request, 'sd/register.html')


def create_account(request):
    page = 'sd/create_account.html'
    return render(request, page)

# https://stackoverflow.com/questions/18284010/django-modelform-not-saving-data-to-database


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
    # pdb.set_trace()
    if request.method == "GET":
        return render(request, 'sd/login.html')

    info = request._post
    user_name = info['username']
    pass_word = info['password']
    try:
        user = Author.objects.get(username=user_name)
    except:
        request.session['authenticated'] = False
        return redirect('login')

    if pass_word != user.password:
        return redirect('login')

    request.session['authenticated'] = True
    key = Author.objects.get(username=user_name).uuid
    request.session['auth-user'] = str(key)
    request.session['SESSION_EXPIRE_AT_BROWSER_CLOSE'] = True
    return redirect('my_feed')


def logout(request):
    try:
        request.session['authenticated'] = False
        request.session.pop('auth-user')
        request.session.flush()
    except KeyError as k:
        print("Not currently authenticated, returning to feed")
    return redirect('explore')


def new_post(request):
    token = request.headers['Cookie'].split('=')[1]
    if not Token.objects.filter(key=token):
        return redirect('login')

    if request.method == "POST":
        data = request.POST.copy()
        # data['author'] = Author.objects.get(auth_token=token)
        print(data)
        form = NewPostForm(data)
        if form.is_valid():
            # print("VALID")
            # form.save(commit=False)
            pdb.set_trace()
            form.author = Token.objects.get(
                user_id=request.session['Set-Cookie']['sessionid'])
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


def feed(request):
    if authenticated(request):
        print("VERIFIED LOGIN")
        user = get_current_user(request)
        print(user.username+" IS LOGGED IN")
        page = 'sd/feed.html'
        return render(request, page, {'current_user': user})
    else:
        print("NOT LOGGED IN")
        page = 'sd/index.html'
        return render(request, page)