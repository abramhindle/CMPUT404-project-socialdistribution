from django.http import *
from service.models.author import Author
from service.models.inbox import Inbox
from service.models.post import Post
from service.models.comment import Comment
from service.models.follow import Follow
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

        page = int(request.GET.get('page', 1))
        size = int(request.GET.get('size', 5))

        try:
            self.author = Author.objects.get(_id=self.author_id)
        except ObjectDoesNotExist:
            return HttpResponseNotFound()
        
        try:
            self.inbox = Inbox.objects.get(author=self.author) #author_id is the primary key for an inbox
        except ObjectDoesNotExist:
            inbox_json = {
                "type": "inbox",
                "author": str(self.author_id),
                "items": list()
            }
            return HttpResponse(json.dumps(inbox_json), content_type = CONTENT_TYPE_JSON)

        posts = self.inbox.posts.all()
        comments = self.inbox.comments.all()
        follow_requests = self.inbox.follow_requests.all()

        inbox_items = list(posts) + list(comments) + list(follow_requests)

        inbox_items.sort(key=lambda x: x.published, reverse=True) #TODO: this needs to be optimized

        paged_inbox_items = list()

        for i in range(0, page): # do this for as many times as we need for paging
            #get size of items out of inbox_items
            paged_inbox_items = inbox_items[0:size]
            inbox_items = inbox_items[size:]

        for i in range(0, len(paged_inbox_items)):
            paged_inbox_items[i] = paged_inbox_items[i].toJSON()

        inbox_json = {
            "type": "inbox",
            "author": str(self.author_id),
            "items": paged_inbox_items
        }

        return HttpResponse(json.dumps(inbox_json), content_type = CONTENT_TYPE_JSON)

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

        try:    #TODO check if requires additional tweaking
            if body["data"]["type"] == "post":
                id = body["data"]["id"]
                self.handle_post(inbox, id, body["data"], self.author)
            elif body["type"] == "comment":
                id = body["id"]
                self.handle_comment(inbox, id, body, self.author)
            elif body["type"] == "follow": #TODO: fill these in once the objects are done
                id = Follow.create_follow_id(body["object"]["id"], body["actor"]["id"])
                self.handle_follow(inbox, id, body, self.author)
            elif body["type"] == "like":
                pass
            else:
                return HttpResponseBadRequest()

        except KeyError:
            return HttpResponseBadRequest()
        except ObjectDoesNotExist:
            return HttpResponseNotFound()
        except ConflictException:
            return HttpResponse(status=409)
        
        inbox.save()

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

        #delete all follow requests
        #TODO: maybe a different endpoint for this later?
        follow_requests = self.inbox.follow_requests.all()

        for follow_request in follow_requests:
            follow_request.delete()

        self.inbox.delete()

        return HttpResponse(status=202)
    
    def handle_post(self, inbox: Inbox, id, body, author):
        post = inbox.posts.all().filter(_id=id)

        #TODO: make request and PUT post to DB if it isnt already there -> for now, we assume it IS there
        # post_author = body["author"]["id"]
        # post_id = body["id"]
        # url = f"{settings.DOMAIN}/authors/{post_author}/posts/{post_id}"
        # requests.put()

        if post.exists():
            raise ConflictException #conflict, item is already in inbox

        post = Post.objects.get(_id=id)
        inbox.posts.add(post)

    def handle_comment(self, inbox: Inbox, id, body, author):
        comment = inbox.comments.all().filter(_id=id)
        
        if comment.exists():
            raise ConflictException #conflict, item is already in inbox

        comment = Comment.objects.get(_id=id)
        inbox.comments.add(comment)

    def handle_follow(self, inbox: Inbox, id, body, author: Author): #we actually create the follow request here
        follow_req = inbox.follow_requests.all().filter(_id=id)

        if follow_req.exists():
            raise ConflictException

        foreign_author = Author()
        foreign_author.toObject(body["actor"])

        try:
            author.followers.get(_id=foreign_author._id)
        except ObjectDoesNotExist: #only create request if they are NOT already being followed
            follow_request = Follow.objects.create(actor=foreign_author, object=author)
            inbox.follow_requests.add(follow_request)
    

class ConflictException(Exception):
    pass