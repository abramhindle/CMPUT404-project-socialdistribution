from django.http.request import HttpRequest
from django.http.response import HttpResponse, HttpResponseBadRequest, HttpResponseNotFound
from django.views import View
from .dto_models import Author
from django.apps import apps
from django.views.decorators.csrf import csrf_exempt
from django.http.response import HttpResponse, HttpResponseNotFound
from django.shortcuts import render
from django.views import generic

from rest_framework.views import APIView
from rest_framework.request import Request
User = apps.get_model('core', 'User')
from rest_framework import viewsets
from rest_framework import response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.permissions import IsAuthenticated

# Create your views here.

class author(View):
    def get(self, request: HttpRequest, author_id: str):
        user: User = User.objects.get(pk=author_id)
        if (user):
            host = request.get_host()
            return HttpResponse(Author.from_user(user, host).to_json())
        else:
            return HttpResponseNotFound()

    @csrf_exempt 
    def post(self, request: HttpRequest, author_id: str):
        user: User = User.objects.get(pk=author_id)

        if (user):
            host = request.get_host()
            author = Author.from_body(request.body)
            if (author.get_user_id() != str(user.id)):
                return HttpResponseBadRequest("The id of the author in the body does not match the author_id in the request.")
            
            if (author.type != "author"):
                return HttpResponseBadRequest("Can not change the type of an author")

            user = author.merge_user(user)
            user.save()
            return HttpResponse(Author.from_user(user, host).to_json())
        else:
            return HttpResponseNotFound()

class authors(View):
    def get(self, request: HttpRequest):
        host = request.get_host()
        users = User.objects.all()
        authors = list(map(lambda x: Author.from_user(x, host), users))

        return HttpResponse(Author.list_to_json(authors))

def getAuthor(author_id: str) -> Author:
    try:
        author = User.objects.get(id=author_id)
    except:
        return None
    return author


def getFollower(author: User, follower_id: str) -> Author:
    try:
        follower = author.followers.get(id=follower_id)
    except:
        return None
    return follower


class FollowerDetails(APIView):
    def get(self, request: HttpRequest, author_id: str, foreign_author_id: str = None):
        author = getAuthor(author_id)
        if not author:
            return HttpResponseNotFound("Database could not find author")
        if foreign_author_id:
            follower = getFollower(author, foreign_author_id)
            if not follower:
                return HttpResponseNotFound("Foreign author id not found in database")
            return Response('follower data in serialized format',status=200)
        allFollowers = list(author.followers.all())
        followers_dic={"type":"followers",
                       "items":Author.list_to_json(allFollowers)}
        return Response(followers_dic,status=200)

    def delete(self, request: Request, author_id: str,foreign_author_id: str):
        author = getAuthor(author_id)
        if not author:
            return HttpResponseNotFound("Database could not find author")
        follower=getFollower(author,foreign_author_id)
        if not follower:
            return HttpResponseNotFound("Database could not find follower")
        author.followers.remove(follower)
        return Response({"detail":"id {} successfully removed".format(follower.id)},status=200)

    def put(self, request: Request, author_id: str, foreign_author_id:str):
        author = getAuthor(author_id)
        if not author:
            return HttpResponseNotFound("Database could not find author")
        follower = getFollower(author, foreign_author_id)
        if not follower:
            return HttpResponseNotFound("Database could not find follower")
        author.followers.add(follower)

        return Response({"detail":"id {} successfully added".format(follower.id)},status=200)