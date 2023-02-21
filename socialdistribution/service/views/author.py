from django.http import *
from service.models.author import Author
from service.service_constants import *

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
import json

from django.views.decorators.csrf import csrf_exempt

# Create your views here.

def multiple_authors(request: HttpRequest):
    if request.method == GET:
        print(request.user.is_authenticated)
        authors_queryset = Author.objects.all().order_by('displayName')
        page = request.GET.get('page', '')
        size = request.GET.get('size', '')

        if not page or not size:
            return HttpResponseBadRequest()

        paged_authors = Paginator(authors_queryset, size)

        try:
            page = paged_authors.page(page)
        except:
            page = list()
        
        authors = list()

        for author in page:
            authors.append(encode_json(author))

        authors = encode_list(authors)

        return HttpResponse(json.dumps(authors), content_type = CONTENT_TYPE_JSON)

    return HttpResponseNotAllowed()

@csrf_exempt #TODO: remove
def single_author(request: HttpRequest, id):
    if request.method == GET:
        try:
            author = Author.objects.get(_id=id)
        except:
            author = None

        if not author:
            return HttpResponseNotFound()

        author_json = encode_json(author)

        return HttpResponse(json.dumps(author_json), content_type = CONTENT_TYPE_JSON)
    
    elif request.method == POST:

        body = request.body.decode(UTF8)
        body = json.loads(body)

        try:
            author = Author.objects.get(_id=id)
        except:
            return HttpResponseNotFound()

        if "displayName" in body:
            author.displayName = body["displayName"]

        if "github" in body:
            author.github = body["github"]

        if "profileImage" in body:
            author.profileImage = body["profileImage"]

        author.save() #updates whatever is set in the above if statements

        author_json = encode_json(author)

        return HttpResponse(json.dumps(author_json), status=202, content_type = CONTENT_TYPE_JSON)
    return HttpResponseNotAllowed()

def encode_json(author: Author):
    return {
            "type": "author",
            "id": str(author._id),
            "host": author.host,
            "displayName": author.displayName,
            "url": f"{author.host}/authors/{author._id}", #generated here
            "github": author.github,
            "profileImage": author.profileImage,
    }

def encode_list(authors: list[Author]):
    return {
        "type": "author",
        "items": authors
    }