from django.http.request import HttpRequest
from django.http.response import Http404, HttpResponse, HttpResponseBadRequest, HttpResponseNotFound, JsonResponse
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from apps.core.serializers import AuthorSerializer
from apps.core.models import Author
from rest_framework.parsers import JSONParser
from socialdistribution.utils import Utils
import json


def getAuthor(author_id: str) -> Author:
    try:
        author = Author.objects.get(pk=author_id)
    except:
        raise Http404()
    return author


def getFollower(author: Author, follower_id: str) -> Author:
    try:
        follower = author.followers.get(pk=follower_id)
    except:
        return None
    return follower


class author(GenericAPIView):
    def get(self, request: HttpRequest, author_id: str):
        author: Author = getAuthor(author_id)

        if (author):
            host = request.scheme + "://" + request.get_host()
            serializer = AuthorSerializer(author, context={'host': host})
            return HttpResponse(Utils.serialize(serializer, request))
        else:
            return HttpResponseNotFound()
        

    def post(self, request: HttpRequest, author_id: str):
        author: Author = getAuthor(author_id)

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
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return HttpResponseNotFound()

class authors(GenericAPIView):
    def get(self, request: HttpRequest):
        host = request.scheme + "://" + request.get_host()
        authors = self.filter_queryset(Author.objects.all())
        one_page_of_data = self.paginate_queryset(authors)
        serializer = AuthorSerializer(one_page_of_data, context={'host': host}, many=True)
        dict_data = Utils.formatResponse(query_type="GET on authors", data=serializer.data)
        result = self.get_paginated_response(dict_data)
        return JsonResponse(result.data, safe=False)


# GET all authors
# curl 127.0.0.1:8000/authors

# GET a single author
# curl 127.0.0.1:8000/author/<author_id>
# curl 127.0.0.1:8000/author/4f890507-ad2d-48e2-bb40-163e71114c27

# POST to update a single author. Get "yourtoken" from storage in your browser after loging in. Note the single quotes around data
# curl -d 'yourdata' 127.0.0.1:8000/author/<author_id> -H "X-CSRFToken: yourtoken" -H "Cookie: csrftoken=yourtoken" 
# curl -d '{"type": "author", "id": "a1fcf249-528a-4e8a-912c-eef7a4470696", "displayName": "Author","github": "","profileImage": ""}' 127.0.0.1:8000/author/a1fcf249-528a-4e8a-912c-eef7a4470696 -H "X-CSRFToken: DvubOcnWbnd5jfQpDGzQYGDMsz7RLIu345gPWbv01G9IQSBIOSlNuKWx1Z4ognlT" -H "Cookie: csrftoken=DvubOcnWbnd5jfQpDGzQYGDMsz7RLIu345gPWbv01G9IQSBIOSlNuKWx1Z4ognlT" 

class FollowerDetails(GenericAPIView):
    def get(self, request: HttpRequest, author_id: str, foreign_author_id: str = None):
        author = getAuthor(author_id)
        host = request.scheme + "://" + request.get_host()
        if not author:
            return HttpResponseNotFound("Database could not find author")
        if foreign_author_id:
            follower = getFollower(author, foreign_author_id)
            if not follower:
                return HttpResponseNotFound("Foreign author id not found in database")

            serializer = AuthorSerializer(follower, context={'host': host})
            return HttpResponse(Utils.serialize(serializer, request))

        allFollowers = self.filter_queryset(author.followers.all())
        one_page_of_data = self.paginate_queryset(allFollowers)
        serializer = AuthorSerializer(one_page_of_data, context={'host': host}, many=True)
        dict_data = Utils.formatResponse(query_type="GET on authors", data=serializer.data)
        result = self.get_paginated_response(dict_data)
        followers_dic = {"type": "followers",
                         "items": result.data}
        return JsonResponse(followers_dic, safe=False)

    def delete(self, request: HttpRequest, author_id: str, foreign_author_id: str):
        author = getAuthor(author_id)
        if not author:
            return HttpResponseNotFound("Database could not find author")
        follower = getFollower(author, foreign_author_id)
        if not follower:
            return HttpResponseNotFound("Database could not find follower")
        author.followers.remove(follower)
        author.save()
        return Response({"detail": "id {} successfully removed".format(follower.id)}, status=200)

    def put(self, request: HttpRequest, author_id: str, foreign_author_id: str):
        author = getAuthor(author_id)
        if not author:
            return HttpResponseNotFound("Database could not find author")
        follower = getAuthor(foreign_author_id)
        if not follower:
            return HttpResponseNotFound("Database could not find follower")
        author.followers.add(follower)
        author.save()
        return Response({"detail": "id {} successfully added".format(follower.id)}, status=200)

# GET follower
# curl 127.0.0.1:8000/author/4f890507-ad2d-48e2-bb40-163e71114c27/followers

# GET follower
# curl 127.0.0.1:8000/author/4f890507-ad2d-48e2-bb40-163e71114c27/followers/9f48208f-372a-45e6-a024-2b9750c9b494

# PUT follower
# curl -X PUT 127.0.0.1:8000/author/4f890507-ad2d-48e2-bb40-163e71114c27/followers/9f48208f-372a-45e6-a024-2b9750c9b494