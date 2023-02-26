from django.http import *
from service.models.author import Author
from service.models.inbox import Inbox
from service.models.post import Post
from service.models.comment import Comment
from service.service_constants import *
from django.views import View
from django.core.exceptions import ObjectDoesNotExist

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
import json
import uuid

#import requests #TODO: decide if we are ok with using requests to make object creation requests

from django.utils.decorators import method_decorator

from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.conf import settings

# flow of endpoints
# -> POST post for {author_id} -> for {follower_author_id} of {author_id} of post (POST Inbox {follower author Id})

@method_decorator(csrf_exempt, name='dispatch')
class InboxView(View):
    ["get", "post", "delete"]

    def get(self, request: HttpRequest, *args, **kwargs):
        self.author_id = kwargs['author_id']

        page = request.GET.get('page', 1)
        size = request.GET.get('size', 5)

        try:
            self.author = Author.objects.get(_id=self.author_id)
            self.inbox = Inbox.objects.get(author=self.author) #author_id is the primary key for an inbox
        except ObjectDoesNotExist:
            return HttpResponseNotFound()
        
        posts = self.inbox.posts.all()
        comments = self.inbox.comments.all()

        inbox_items = list(posts) + list(comments)

        inbox_items.sort(key=lambda x: x.published, reverse=True) #TODO: this needs to be optimized

        paged_inbox = list()

        for i in range(0, page): # do this for as many times as we need for paging
            #get size of items out of inbox_items
            paged_inbox = inbox_items[0:size]
            inbox_items = inbox_items[size:]

        for i in range(0, len(paged_inbox)):
            paged_inbox[i] = paged_inbox[i].toJSON()

        return HttpResponse(json.dumps(paged_inbox), content_type = CONTENT_TYPE_JSON)

    def post(self, request: HttpRequest, *args, **kwargs):
        self.author_id = kwargs['author_id']

        body = request.body.decode(UTF8)
        body = json.loads(body)

        try:
            self.author = Author.objects.get(_id=self.author_id)
        except ObjectDoesNotExist:
            return HttpResponseNotFound()

        try: # if inbox is empty, it will likely not exist yet, so we need to either get it or instantiate it
            inbox = Inbox.objects.get(author=self.author) #author_id is the primary key for an inbox
        except ObjectDoesNotExist:
            inbox = Inbox.objects.create(author=self.author)

        try:
            id = body["id"]

            if body["type"] == "post":
                post = inbox.posts.all().filter(_id=id)

                if post.exists():
                    return HttpResponse(status=409) #conflict, item is already in inbox

                post = Post.objects.get(_id=id)
                inbox.posts.add(post)

            elif body["type"] == "comment":
                post = inbox.comments.all().filter(_id=id)
                
                if post.exists():
                    return HttpResponse(status=409) #conflict, item is already in inbox

                comment = Comment.objects.get(_id=id)
                inbox.comments.add(comment)

            elif body["type"] == "follow": #TODO: fill these in once the objects are done
                pass
            elif body["type"] == "comment":
                pass
            else:
                return HttpResponseBadRequest()

        except KeyError:
            return HttpResponseBadRequest()
        except ObjectDoesNotExist:
            return HttpResponseBadRequest()
        
        return HttpResponse(status=202)

    def delete(self, request: HttpRequest, *args, **kwargs):
        self.author_id = kwargs['author_id']

        try:
            self.author = Author.objects.get(_id=self.author_id)
        except ObjectDoesNotExist:
            return HttpResponseNotFound()

        try:
            self.inbox = Inbox.objects.get(author=self.author) #already deleted
        except ObjectDoesNotExist:
            return HttpResponse(status=202)

        self.inbox.delete()

        return HttpResponse(status=202) 

#TODO: when handling cross domain requests, at this step we WILL need to fetch post or author information from a remote host
# and store a copy on this server if that author or post doesn't already exist on our local, for now
    def handle_post(self, inbox: Inbox, post_id):
        try:
            post = inbox.posts.get(_id=post_id)
        except ObjectDoesNotExist:
            #CREATE OBJECT
            raise ObjectDoesNotExist #TODO: placeholder, this will get filled in I just wanted to outline the structure
        inbox.posts.add(post)
        
    def handle_comment(self, inbox: Inbox, comment_id):
        try:
            comment = inbox.comments.get(_id=comment_id)
        except ObjectDoesNotExist:
            #CREATE OBJECT
            raise ObjectDoesNotExist #TODO: placeholder, this will get filled in I just wanted to outline the structure
        inbox.posts.add(comment)