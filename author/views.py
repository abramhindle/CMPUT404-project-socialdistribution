from functools import partial
import json

from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth import login as django_login
from django.contrib.auth import logout as django_logout
from django.contrib.auth.models import User
from django.core.paginator import (EmptyPage, InvalidPage, PageNotAnInteger,
                                   Paginator)
from django.db.models import Subquery
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.utils import timezone
from django.views.decorators.http import require_GET, require_http_methods
from rest_framework.authentication import (BasicAuthentication,
                                           SessionAuthentication)
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from author import serializers

from .models import Author, Follow, Inbox
from post.models import Like
from .serializers import AuthorSerializer
from post.serializers import LikeSerializer


class index(APIView):
    def get(self, request):
        '''
        GET: retrieve all profiles on the server paginated
            * If no page and size are given, returns all authors instead
            * If invalid parameters are given e.g. size = 0, negative page number, sends 400 Bad Request
        '''

        author_query = Author.objects.all().order_by("authorID")
        param_page = request.GET.get("page", None)
        param_size = request.GET.get("size", None)
        if param_page != None and param_size != None:
            authorPaginator = Paginator(author_query, param_size)
            authors_data = []
            try:
                authors_data = AuthorSerializer(authorPaginator.page(param_page), many=True).data
            except (PageNotAnInteger, ZeroDivisionError):
                # bad request where page is not a number
                return Response(status=400)
            except EmptyPage:
                pass

            response = {
                "type": "authors",
                "items": authors_data
            }
            return Response(response)
        else:
            # return all authors
            author_query = Author.objects.all().order_by("authorID")
            authors_data = AuthorSerializer(author_query, many=True).data
            response = {
                "type": "authors",
                "items": authors_data
            }
            return Response(response)

    # def post(self, request):
    #     author_data = JSONParser().parse(request)
    #     author_serializer = AuthorCreationSerializer(data=author_data)
    #     if author_serializer.is_valid():
    #         author_serializer.save()
    #         return JsonResponse(author_serializer.data, status=201)
    #     else:
    #         print(author_serializer.errors)
    #     return Response(status=422)


class profile(APIView):
    def get(self, request, author_id):
        try:
            author_profile = Author.objects.get(authorID=author_id)
            serializer = AuthorSerializer(author_profile)
            return Response(serializer.data)
        except Author.DoesNotExist:
            return Response("This author does not exist", status=404)

    def post(self, request, author_id):
        # TODO: add authentication for profile creation/updates
        try:
            author = Author.objects.get(authorID=author_id)
            update_data = JSONParser().parse(request)
            serializer = AuthorSerializer(author, data=update_data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse(serializer.data, status=201)
            print(serializer.errors)
            return Response(status=422)
        except Author.DoesNotExist:
            new_data = JSONParser().parse(request)
            serializer = AuthorSerializer(
                data=new_data,
                context={"authorID": author_id})
            if serializer.is_valid():
                serializer.save()
                return JsonResponse(serializer.data, status=201)
            print(serializer.errors)
            return JsonResponse(serializer.data, status=201)


class login(APIView):
    def post(self, request):
        try:
            username = request.POST['username']
            password = request.POST['password']
        except:
            return Response("Bad request. The expected keys 'username' and 'password' were not found.", status=400)
        user = authenticate(request=request, username=username, password=password)
        if user is not None:
            author_serializer = AuthorSerializer(user.author)
            django_login(request, user)
            return Response(author_serializer.data, status=200)
        else:
            return Response("Invalid login credentials.", status=401)


class logout(APIView):
    def post(self, request):
        django_logout(request)
        return Response(status=200)


class register(APIView):
    def post(self, request):
        try:
            username = request.POST['username']
            password = request.POST['password']
        except:
            return Response("Bad request. The expected keys 'username' and 'password' were not found.", status=400)
        if User.objects.filter(username=username).exists():
            # The user already exists
            return Response("The given username is already in use.", status=409)
        user = User.objects.create_user(username=username, password=password)
        user.is_active = False
        user.save()
        author = Author(user=user, host=request.build_absolute_uri('/'))
        author.save()
        return Response("A new user was created.", status=201)


class followers(APIView):
    def get(self, request, author_id):
        try:
            author = Author.objects.get(authorID=author_id)
        except:
            # The author does not exist
            return Response(status=404)
        follower_ids = Follow.objects.filter(toAuthor=author_id)
        follower_profiles = Author.objects.filter(authorID__in=follower_ids.values_list('fromAuthor', flat=True))
        serializer = AuthorSerializer(follower_profiles, many=True)
        response = {'type': 'followers', 'items': serializer.data}
        return Response(response)


class follower(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    #permission_classes = [IsAuthenticated]

    def get(self, request, author_id, foreign_author_id):
        follower = Follow.objects.filter(toAuthor=author_id, fromAuthor=foreign_author_id)
        if not follower:
            return Response(status=404)
        else:
            return Response(status=200)

    def put(self, request, author_id, foreign_author_id):
        if request.user.is_authenticated:
            try:
                author = request.user.author
            except:
                # The user does not have an author profile
                return Response(status=403)
            if str(author.authorID) != author_id:
                # The request was made by a different author
                return Response(status=403)
            try:
                fromAuthor = Author.objects.get(authorID=foreign_author_id)
            except:
                # The foreign author does not exist
                return Response(status=404)
            if Follow.objects.filter(fromAuthor=fromAuthor, toAuthor=author).exists():
                # The follower already exists
                return Response(status=409)
            # Add the follower
            follow = Follow.objects.create(fromAuthor=fromAuthor, toAuthor=author, date=timezone.now())
            follow.save()
            return Response(status=201)
        else:
            # Request was not authenticated
            return Response(status=401)

    def delete(self, request, author_id, foreign_author_id):
        try:
            Follow.objects.get(fromAuthor=foreign_author_id, toAuthor=author_id).delete()
        except:
            # Nothing to delete
            return Response(status=404)
        return Response(status=200)

class liked(APIView):
    def get(self, request, author_id):
        if not Author.objects.filter(authorID=author_id).exists():
            return Response(status=404)
        liked = Like.objects.filter(fromAuthor=author_id)
        serializer = LikeSerializer(liked, many=True)
        response = {"type": "liked", "items": serializer.data}
        return Response(response, status=200)

class inbox(APIView):
    pass
