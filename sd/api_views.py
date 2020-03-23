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
import os
import pdb
import json
import uuid
from uuid import uuid4


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


class GetAllAuthorsAPIView(APIView):
    serializer_class = AuthorSerializer

    def get(self, request):
        authors = Author.objects.all()
        serializer = AuthorSerializer(authors, many=True)
        return Response(
            serializer.data, status=status.HTTP_200_OK
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
    #   "content": "ExampleBody",
    #   "visibility": "pub",
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
        posts = posts.filter(visibility='pub')
        serializer = GetPostSerializer(posts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class GetAllAuthorFriendsAPIView(APIView):
    authentication_classes = [BasicAuthentication, SessionAuthentication]
    serializer_class = FriendSerializer

    # Returns All Author's friends
    def get(self, request, pk, format=None):
        friends = Friend.objects.filter(author=pk)
        serializer = FriendSerializer(friends, many=True)
        response = {"authors": [x['friend'] for x in serializer.data]}
        return Response(response, status=status.HTTP_200_OK)


class GetAllPublicPostsAPIView(APIView):
    serializer_class = GetPostSerializer

    def get(self, request, format=None):
        posts = Post.objects.filter(visibility='1')
        serializer = GetPostSerializer(posts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class GetAllVisiblePostsAPIView(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = GetPostSerializer

    def get(self, request, format=None):
        userUUID = request.user
        if userUUID == "AnonymousUser":
            posts = Post.objects.filter(visibility='1')
            serializer = GetPostSerializer(posts, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            # -------------
            # public posts
            # -------------

            filteredPosts = Post.objects.filter(visibility='1')

            # -------------
            # foaf posts
            # -------------

            foafPosts = Post.objects.filter(visibility='2')

            friends = Friend.objects.filter(author=userUUID).union(
                Friend.objects.filter(friend=userUUID))

            foafUUIDs = []
            friendUUIDs = []
            # for each friend
            for friend in friends:
                # append friend's uuid to foaf
                if friend.friend not in foafUUIDs:
                    foafUUIDs.append(friend.friend)
                    friendUUIDs.append(friend.friend)

                # innerFriends is friend's friends
                innerFriend = Friend.objects.filter(author=friend.friend)
                for f2 in innerFriend:
                    if f2.friend not in foafUUIDs:
                        foafUUIDs.append(f2.friend)

            for uuid in foafUUIDs:
                filteredPosts.union(foafPosts.filter(author=uuid))

            # -------------
            # friend posts
            # -------------

            friendPosts = Post.objects.filter(visibility='3')

            for uuid in friendUUIDs:
                filteredPosts.union(friendPosts.filter(author=uuid))

            # -------------
            # private posts
            # -------------

            privatePosts = Post.objects.filter(visibility='4')

            filteredPosts.union(privatePosts.filter(author=userUUID))

            # -------------
            # server posts
            # -------------

            author = Author.objects.get(uuid=userUUID)

            serverAuthors = Author.objects.filter(host=author.host)

            serverPosts = Post.objects
            for author in serverAuthors:
                serverPosts.union(Post.objects.filter(
                    author=author.uuid).filter(visibility='5'))

            filteredPosts.union(serverPosts)

            serializer = GetPostSerializer(filteredPosts, many=True)
            return Response(
                serializer.data, status=status.HTTP_200_OK
            )


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


class GetAllFOAFAPIView(APIView):
    serializer_class = AuthorSerializer

    def get(self, request, pk):
        friends = Friend.objects.filter(author=pk)
        foaf = []
        # for each friend
        for friend in friends:
            # append friend's uuid to foaf
            if friend.friend not in foaf:
                foaf.append(friend.friend)

            # innerFriends is friend's friends
            innerFriend = Friend.objects.filter(author=friend.friend)
            for f2 in innerFriend:
                if f2.friend not in foaf:
                    foaf.append(f2.friend)

        authors = []
        for author in foaf:
            if author.uuid != pk:
                authors.append(Author.objects.get(uuid=author.uuid))

        serializer = AuthorSerializer(authors, many=True)
        return Response(
            serializer.data, status=status.HTTP_200_OK
        )


class CreateFriendAPIView(CreateAPIView):
    serializer_class = FriendSerializer

    # pk = uuid of friend request
    def create(self, request, pk):
        friendRequest = FriendRequest.objects.get(uuid=pk)

        data = {}
        data['friend'] = friendRequest.__dict__['to_author_id']
        data['author'] = friendRequest.__dict__['from_author_id']

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            {**serializer.data},
            status=status.HTTP_201_CREATED,
            headers=headers
        )


class DeleteFriendAPIView(APIView):

    def delete(self, request, pk, format=None):
        currentUser = request.user
        # determine if user is Friend object's "author" or "friend"
        try:
            friend = Friend.objects.get(author=pk, friend=currentUser)
        except Exception:
            try:
                friend = Friend.objects.get(author=currentUser, friend=pk)
            except Exception:
                print("Friendship doesn't exist!")
                return Response(
                    status=status.HTTP_404_NOT_FOUND
                )
        friend.delete()
        return Response(
            status=status.HTTP_204_NO_CONTENT
        )
