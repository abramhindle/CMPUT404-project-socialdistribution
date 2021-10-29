from django.http.request import HttpRequest
from django.http.response import Http404, HttpResponse, HttpResponseBadRequest, HttpResponseNotFound
from django.views import View
from apps.core.serializers import AuthorSerializer
from apps.core.models import Author
from rest_framework.parsers import JSONParser
from socialdistribution.utils import Utils

# Create your views here.

class author(View):
    def get(self, request: HttpRequest, author_id: str):
        author: Author = None
        try:
            author: Author = Author.objects.get(pk=author_id)
        except:
            return Http404()

        if (author):
            host = request.scheme + "://" + request.get_host()
            serializer = AuthorSerializer(author, context={'host': host})

            return HttpResponse(Utils.serialize(serializer, request))
        else:
            return HttpResponseNotFound()
        

    def post(self, request: HttpRequest, author_id: str):
        author: Author = None
        try:
            author: Author = Author.objects.get(pk=author_id)
        except:
            return Http404()

        if (author):
            host = request.scheme + "://" + request.get_host()

            data = JSONParser().parse(request)
            serializer = AuthorSerializer(data=data)

            if (serializer.is_valid()):
                if (data.__contains__("host") and data['host'] != host):
                    return HttpResponseBadRequest("The author is not from a supported host.")

                if (not data.__contains__("id") and data['id'] != str(author.id)):
                    return HttpResponseBadRequest("The id of the author in the body does not match the author_id in the request.")
            
                if (data.__contains__("type") and data['type'] != "author"):
                    return HttpResponseBadRequest("Can not change the type of an author")

                if (data.__contains__("displayName") and data['displayName'] != author.displayName):
                    author.displayName = data['displayName']

                author.github = data['github']
                author.profileImage = data['profileImage']
                author.save()

                return HttpResponse(Utils.serialize(AuthorSerializer(author, context={'host': host}), request))
            else:
                HttpResponseBadRequest("Invalid data")
        else:
            return HttpResponseNotFound()

class authors(View):
    def get(self, request: HttpRequest):
        host = request.scheme + "://" + request.get_host()
        authors = Author.objects.all()
        serializer = AuthorSerializer(authors, context={'host': host}, many=True)
        return HttpResponse(Utils.serialize(serializer, request))


# GET all authors
# curl 127.0.0.1:8000/authors -H 'Accept: application/json; indent=4'

# GET a single author
# curl 127.0.0.1:8000/author/<author_id> -H 'Accept: application/json; indent=4'
# curl 127.0.0.1:8000/author/9a70f95c-d72b-43af-b8f7-35ce111cfea8 -H 'Accept: application/json; indent=4'

# POST to update a single author. Get "yourtoken" from storage in your browser after loging in. Note the single quotes around data
# curl -d 'yourdata' 127.0.0.1:8000/author/<author_id> -H "X-CSRFToken: yourtoken" -H "Cookie: csrftoken=yourtoken" 
# curl -d '{"type": "author", "id": "9a70f95c-d72b-43af-b8f7-35ce111cfea8", "displayName": "Author","github": "","profileImage": ""}' 127.0.0.1:8000/author/9a70f95c-d72b-43af-b8f7-35ce111cfea8 -H "X-CSRFToken: DvubOcnWbnd5jfQpDGzQYGDMsz7RLIu345gPWbv01G9IQSBIOSlNuKWx1Z4ognlT" -H "Cookie: csrftoken=DvubOcnWbnd5jfQpDGzQYGDMsz7RLIu345gPWbv01G9IQSBIOSlNuKWx1Z4ognlT" 

from django.http.request import HttpRequest
from django.http.response import HttpResponse, HttpResponseBadRequest, HttpResponseNotFound
from django.views import View
from apps.core.models import Author
from django.apps import apps
from django.views.decorators.csrf import csrf_exempt
from django.http.response import HttpResponse, HttpResponseNotFound
from django.shortcuts import render
from django.views import generic

from rest_framework.views import APIView
from rest_framework.request import Request
import json
User = apps.get_model('core', 'User')
from rest_framework import viewsets
from rest_framework import response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.permissions import IsAuthenticated


# Create your views here.




def getAuthor(author_id: str) -> Author:
    try:
        author = Author.objects.get(pk=author_id)
    except:
        return None
    return author


def getFollower(author: Author, follower_id: str) -> Author:
    try:
        follower = author.followers.get(pk=follower_id)
    except:
        return None
    return follower


class FollowerDetails(APIView):
    def get(self, request: Request, author_id: str, foreign_author_id: str = None):
        author = getAuthor(author_id)
        if not author:
            return HttpResponseNotFound("Database could not find author")
        if foreign_author_id:
            follower = getFollower(author, foreign_author_id)
            if not follower:
                return HttpResponseNotFound("Foreign author id not found in database")
            return Response('follower data in serialized format', status=200)
        allFollowers = list(author.followers.all())
        jsonList=[]
        for otherFollowers in allFollowers:
            jsonList.append(json.dumps(otherFollowers.__dict__))
        finalJson=",".join(jsonList)
        followers_dic = {"type": "followers",
                         "items": finalJson}
        return Response(followers_dic, status=200)

    def delete(self, request: Request, author_id: str, foreign_author_id: str):
        author = getAuthor(author_id)
        if not author:
            return HttpResponseNotFound("Database could not find author")
        follower = getFollower(author, foreign_author_id)
        if not follower:
            return HttpResponseNotFound("Database could not find follower")
        author.followers.remove(follower)
        author.save()
        return Response({"detail": "id {} successfully removed".format(follower.id)}, status=200)

    def put(self, request: Request, author_id: str, foreign_author_id: str):
        author = getAuthor(author_id)
        if not author:
            return HttpResponseNotFound("Database could not find author")
        follower = getFollower(author, foreign_author_id)
        if not follower:
            return HttpResponseNotFound("Database could not find follower")
        author.followers.add(follower)
        author.save()
        return Response({"detail": "id {} successfully added".format(follower.id)}, status=200)