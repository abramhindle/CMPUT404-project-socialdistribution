import json

from django.core.paginator import Paginator
from django.http import *
from django.views import View

from service.models.author import Author
from service.service_constants import *
from rest_framework.views import APIView

# Create your views here.

class MultipleAuthors(APIView):
    http_method_names = ["get"]

    def get(self, request: HttpRequest, *args, **kwargs):
        authors_queryset = Author.objects.all().order_by('displayName')
        page = request.GET.get('page', 1)
        size = request.GET.get('size', 5)

        paged_authors = Paginator(authors_queryset, size)

        try:
            page = paged_authors.page(page)
        except:
            page = list()

        authors = list()

        for author in page:
            authors.append(author.toJSON())

        authors = encode_list(authors)

        return HttpResponse(json.dumps(authors), content_type=CONTENT_TYPE_JSON)

class SingleAuthor(APIView):
    http_method_names = ["get", "post"]

    def get(self, request, *args, **kwargs):
        author_id = kwargs['author_id']

        try:
            author = Author.objects.get(_id=author_id)
        except:
            author = None

        if not author:
            return HttpResponseNotFound()

        author_json = author.toJSON()

        return HttpResponse(json.dumps(author_json), content_type=CONTENT_TYPE_JSON)

    def post(self, request: HttpRequest, *args, **kwargs):
        body = request.body.decode(UTF8)
        body = json.loads(body)

        author_id = kwargs['author_id']

        try:
            author = Author.objects.get(_id=author_id)
        except:
            return HttpResponseNotFound()

        if "displayName" in body:
            author.displayName = body["displayName"]

        if "github" in body:
            author.github = body["github"]

        if "profileImage" in body:
            author.profileImage = body["profileImage"]

        author.save() #updates whatever is set in the above if statements

        author_json = author.toJSON()

        return HttpResponse(json.dumps(author_json), status=202, content_type=CONTENT_TYPE_JSON)


def encode_list(authors):
    return {
        "type": "author",
        "items": authors
    }


