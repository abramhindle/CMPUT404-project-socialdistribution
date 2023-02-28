from django.http import *
from service.models.author import Author
from service.service_constants import *
from django.views import View

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
import json

import uuid

from django.utils.decorators import method_decorator

from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

# Create your views here.

class MultipleAuthors(View):
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

        return HttpResponse(json.dumps(authors), content_type = CONTENT_TYPE_JSON)

class SingleAuthor(View):
    http_method_names = ["get", "post"]

    def get(self, request, *args, **kwargs):
        self.id = kwargs['author_id']

        try:
            author = Author.objects.get(_id=self.id)
        except:
            author = None

        if not author:
            return HttpResponseNotFound()

        author_json = author.toJSON()

        return HttpResponse(json.dumps(author_json), content_type = CONTENT_TYPE_JSON)
    
    def post(self, request: HttpRequest, *args, **kwargs):
        body = request.body.decode(UTF8)
        body = json.loads(body)

        self.id = kwargs['author_id']

        try:
            author = Author.objects.get(_id=self.id)
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

        return HttpResponse(json.dumps(author_json), status=202, content_type = CONTENT_TYPE_JSON)

def encode_list(authors):
    return {
        "type": "author",
        "items": authors
    }