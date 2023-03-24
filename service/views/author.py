import json

import requests
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import *
from rest_framework.views import APIView

from service.models.author import Author
from service.service_constants import *
from service.services import team_14, team_22


# Create your views here.

class MultipleAuthors(APIView):
    http_method_names = ["get"]

    def get(self, request: HttpRequest, *args, **kwargs):

        filter_host = Q(host=settings.DOMAIN) | Q(host="http://localhost")

        if request.user.username not in [host[0] for host in settings.REMOTE_USERS]:  # if not remote host
            for remote_host in settings.REMOTE_USERS:
                if remote_host[0] == "remote-user-t14":
                    team_14.get_multiple_authors()
                elif remote_host[0] == "remote-user-t22":
                    team_22.get_multiple_authors()

            filter_host = Q()  # no filter, since not a remote user

        authors_queryset = Author.objects.all().order_by('displayName').filter(filter_host)
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
        except ObjectDoesNotExist:
            author = None

        if request.user.username not in [host[0] for host in settings.REMOTE_USERS]:
            if author and author.host == settings.REMOTE_USERS[0][1]:
                author = team_14.get_single_author(author)  # remote-user-t14

            if author and author.host == settings.REMOTE_USERS[1][1]:
                author = team_22.get_single_author(author)  # remote-user-t22

            # put other teams here

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
        except ObjectDoesNotExist:
            return HttpResponseNotFound()

        if "displayName" in body:
            author.displayName = body["displayName"]

        if "github" in body:
            author.github = body["github"]

        if "profileImage" in body:
            author.profileImage = body["profileImage"]

        author.save()  # updates whatever is set in the above if statements

        author_json = author.toJSON()

        return HttpResponse(json.dumps(author_json), status=202, content_type=CONTENT_TYPE_JSON)

def encode_list(authors):
    return {
        "type": "author",
        "items": authors
    }
