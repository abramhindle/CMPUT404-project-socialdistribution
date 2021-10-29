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

