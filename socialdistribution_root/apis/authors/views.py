from django.http.request import HttpRequest
from django.http.response import Http404, HttpResponse, HttpResponseBadRequest, HttpResponseNotFound, JsonResponse
from django.views import View
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from apps.core.serializers import AuthorSerializer
from apps.core.models import Author
from rest_framework.parsers import JSONParser
from socialdistribution.utils import Utils

# Create your views here.

class author(GenericAPIView):
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
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return HttpResponseNotFound()

class authors(GenericAPIView):
    def get(self, request: HttpRequest):
        host = request.scheme + "://" + request.get_host()
        authors = self.filter_queryset(Author.objects.all())
        one_page_of_data = self.paginate_queryset(authors)
        serializer = AuthorSerializer(one_page_of_data, context={'host': host}, many=True)
        dict_data = Utils.compose_posts_dict(query_type="GET on authors", data=serializer.data)
        result = self.get_paginated_response(dict_data)
        return JsonResponse(result.data, safe=False)


# GET all authors
# curl 127.0.0.1:8000/authors

# GET a single author
# curl 127.0.0.1:8000/author/<author_id>
# curl 127.0.0.1:8000/author/a1fcf249-528a-4e8a-912c-eef7a4470696

# POST to update a single author. Get "yourtoken" from storage in your browser after loging in. Note the single quotes around data
# curl -d 'yourdata' 127.0.0.1:8000/author/<author_id> -H "X-CSRFToken: yourtoken" -H "Cookie: csrftoken=yourtoken" 
# curl -d '{"type": "author", "id": "a1fcf249-528a-4e8a-912c-eef7a4470696", "displayName": "Author","github": "","profileImage": ""}' 127.0.0.1:8000/author/a1fcf249-528a-4e8a-912c-eef7a4470696 -H "X-CSRFToken: DvubOcnWbnd5jfQpDGzQYGDMsz7RLIu345gPWbv01G9IQSBIOSlNuKWx1Z4ognlT" -H "Cookie: csrftoken=DvubOcnWbnd5jfQpDGzQYGDMsz7RLIu345gPWbv01G9IQSBIOSlNuKWx1Z4ognlT" 

