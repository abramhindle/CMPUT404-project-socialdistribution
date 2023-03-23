import json

from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator
from django.http import *
from django.views import View

from service.models.author import Author
from service.service_constants import *
from rest_framework.views import APIView

from django.conf import settings

import requests

from django.db.models import Q


# Create your views here.

class MultipleAuthors(APIView):
    http_method_names = ["get"]

    def get(self, request: HttpRequest, *args, **kwargs):

        filter_host = Q(host=settings.DOMAIN) | Q(host="http://localhost")

        # every time we GET all authors, we need to get all authors from other servers and do some updating
        if request.user.username not in [host[0] for host in settings.REMOTE_USERS]:  # if not remote_user, use requests to go out to each remote host and get their values and save them
            # go out to other servers and find all authors and then save them
            # rather than saving the author id we get in the ID, we can save it in the URL, and then create our own ID
            # this means we need to check against URL rather than ID for duplicates

            for remote_host in settings.REMOTE_USERS:
                response = requests.get(remote_host[1] + "service/authors/", auth=remote_host[2])

                if response.status_code < 200 or response.status_code > 299:
                    continue

                response_json = response.json()

                for author in response_json["items"]:
                    if remote_host[0] == "remote-user-t14":
                        handle_t14(author, remote_host[1])

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
        # for the author, if the HOST is remote, reach out to the server and get it from them, then update the current
        # version we have. if the server returns a 404, delete the version we have.

        # we might need something (maybe a job) to routinely check against what we have
        author_id = kwargs['author_id']

        print(author_id)

        try:
            author = Author.objects.get(_id=author_id)
        except ObjectDoesNotExist:
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

#this could probably be a serializer, but i dont care
def handle_t14(author_json, hostname):
    host_url = hostname + str(author_json["id"]) #this is an int

    try:
        # update old -> don't change host_url or id
        old_author = Author.objects.get(url=host_url)

        old_author.github = author_json["github"]
        old_author.profileImage = author_json["profileImage"]
        old_author.displayName = author_json["displayName"]
        old_author.save()
    except ObjectDoesNotExist:
        # create new
        new_author = Author()
        new_author.github = author_json["github"]
        new_author.profileImage = author_json["profileImage"]
        new_author.displayName = author_json["displayName"]
        new_author.url = host_url
        new_author.host = hostname
        new_author.save()

def encode_list(authors):
    return {
        "type": "author",
        "items": authors
    }
