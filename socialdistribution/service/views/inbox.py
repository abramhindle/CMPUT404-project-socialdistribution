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

from django.utils.decorators import method_decorator

from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

# flow of endpoints
# -> POST post for {author_id} -> for {follower_author_id} of {author_id} of post (POST Inbox {follower author Id})

@method_decorator(csrf_exempt, name='dispatch')
class InboxView(View):
    ["get", "post", "delete"]

    def get(self, request: HttpRequest, *args, **kwargs):
        print("http://localhost:8000/authors/author_id/posts/post_id".rsplit('/', 1)[-1])
        return HttpResponse()

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
                self.handle_post(inbox, id)

            elif body["type"] == "comment":
                pass

            elif body["type"] == "follow":
                pass
            elif body["type"] == "comment":
                pass
            else:
                return HttpResponseBadRequest()

        except KeyError:
            return HttpResponseBadRequest()
        except ObjectDoesNotExist:
            return HttpResponseBadRequest()

    def delete(self, request: HttpRequest, *args, **kwargs):
        pass

    def handle_post(self, inbox: Inbox, post_id):
        try:
            post = inbox.posts.get(_id=post_id)
        except ObjectDoesNotExist:
            post = Post.objects.create()
        inbox.posts.add(post)
        
    def handle_comment(self, inbox: Inbox, comment_id):
        try:
            post = inbox.comments.get(_id=comment_id)
        except ObjectDoesNotExist:
            post = Comment.toObject()
        inbox.posts.add(post)
