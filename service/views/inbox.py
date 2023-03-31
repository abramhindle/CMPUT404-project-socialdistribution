import json

from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.http import *
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView

from service.models.author import Author
from service.models.comment import Comment
from service.models.follow import Follow
from service.models.inbox import Inbox
from service.models.like import Like
from service.models.post import Post
from service.service_constants import *
from service.services import team_14, team_16, team_22, team_10

import requests

from rest_framework.permissions import IsAuthenticated

from service.services.inbox_service import handle_follow, handle_post, handle_comment, handle_like, ConflictException


# import requests #TODO: decide if we are ok with using requests to make object creation requests

# flow of endpoints
# -> POST post for {author_id} -> for {follower_author_id} of {author_id} of post (POST Inbox {follower author Id})

@method_decorator(csrf_exempt, name='dispatch')
class InboxView(APIView):
    http_method_names = ["get", "post", "delete"]

    ### GET
    def get(self, request: HttpRequest, *args, **kwargs):
        author_id = kwargs['author_id']

        page = int(request.GET.get('page', 1))
        size = int(request.GET.get('size', 5))

        try:
            author = Author.objects.get(_id=author_id, is_active=True)
        except ObjectDoesNotExist:
            return HttpResponseNotFound()
        
        try:
            inbox = Inbox.objects.get(author=author) #author_id is the primary key for an inbox
        except ObjectDoesNotExist:
            inbox_json = {
                "type": "inbox",
                "author": str(author_id),
                "items": list()
            }
            return HttpResponse(json.dumps(inbox_json), content_type = CONTENT_TYPE_JSON)

        posts = inbox.posts.all()
        comments = inbox.comments.all()
        follow_requests = inbox.follow_requests.all()
        likes = inbox.likes.all()

        inbox_items = list(posts) + list(comments) + list(follow_requests) + list(likes)

        inbox_items.sort(key=lambda x: x.published, reverse=True) #TODO: this needs to be optimized

        paged_inbox_items = list()

        for i in range(0, page): # do this for as many times as we need for paging
            # get size of items out of inbox_items
            paged_inbox_items = inbox_items[0:size]
            inbox_items = inbox_items[size:]

        for i in range(0, len(paged_inbox_items)):
            paged_inbox_items[i] = paged_inbox_items[i].toJSON()

        inbox_json = {
            "type": "inbox",
            "author": str(author_id),
            "items": paged_inbox_items
        }

        return HttpResponse(json.dumps(inbox_json), content_type=CONTENT_TYPE_JSON)

    ### POST
    def post(self, request: HttpRequest, *args, **kwargs):
        self.author_id = kwargs['author_id']

        # try and get author of the inbox
        try:
            author = Author.objects.get(_id=self.author_id, is_active=True)
        except ObjectDoesNotExist:
            return HttpResponseNotFound()

        try:
            body = request.data
        except AttributeError:  # tests don't run without this
            body = request.body
            body = json.loads(body)

        # remote-user-t14
        if author.host == settings.REMOTE_USERS[0][1]:
            response = team_14.handle_inbox(body)
            return HttpResponse(status=202)

        # remote-user-t22
        if author.host == settings.REMOTE_USERS[1][1]:
            #response = team_22.handle_inbox(body)

            #if response is None:
                #return HttpResponseServerError()

            return HttpResponse(status=202)

        # remote-user-t16
        if author.host == settings.REMOTE_USERS[2][1]:
            response = team_16.handle_inbox(body)

            if response is None:
                return HttpResponse(status=503)

            return HttpResponse(status=202)

        # remote-user-t10
        if author.host == settings.REMOTE_USERS[3][1]:
            response = team_10.handle_inbox(body, author)

            if response is None:
                return HttpResponse(status=503)

            return HttpResponse(status=202)

        inbox = self.get_or_create_inbox(author)

        try:
            if body["type"] == "post":
                id = body["id"]
                handle_post(inbox, id, body, author, request.user)
            elif body["type"] == "comment":
                id = body["id"]
                handle_comment(inbox, id, body, author)
            elif body["type"] == "follow" or body["type"] == "Follow":
                handle_follow(inbox, body, author)
            elif body["type"] == "Like":
                #id = Like.create_like_id(body["author"]["id"], body["object"])
                handle_like(inbox, body, author)
            else:
                return HttpResponseBadRequest()

        except KeyError as e:
            print(e)
            return HttpResponseBadRequest()
        except ObjectDoesNotExist:
            return HttpResponseNotFound()
        except ConflictException:
            return HttpResponse(status=409)
        
        inbox.save()

        return HttpResponse(status=202)

    ### DELETE
    def delete(self, request: HttpRequest, *args, **kwargs):
        author_id = kwargs['author_id']

        try:
            author = Author.objects.get(_id=author_id, is_active=True)
        except ObjectDoesNotExist:
            return HttpResponseNotFound()

        try:
            inbox = Inbox.objects.get(author=author) #already deleted

        except ObjectDoesNotExist:
            return HttpResponse(status=202)

        # delete all follow requests
        #TODO: maybe a different endpoint for this later?
        follow_requests = inbox.follow_requests.all()

        for follow_request in follow_requests:
            follow_request.delete()

        inbox.delete()

        return HttpResponse(status=202)

    def get_or_create_inbox(self, author: Author):
        try:  # if inbox is empty, it will likely not exist yet, so we need to either get it or instantiate it
            inbox = Inbox.objects.get(author=author) # author_id is the primary key for an inbox
        except ObjectDoesNotExist:
            inbox = Inbox.objects.create(author=author)

        return inbox
