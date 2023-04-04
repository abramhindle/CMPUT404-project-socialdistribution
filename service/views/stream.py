import json

from django.db.models import Q
from django.http import *
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from service.models.author import Author
from service.models.inbox import Inbox
from service.models.post import Post
from service.service_constants import *
from service.views.post import filter_posts

import service.services.team_10.authors as team_10


#returns an author's stream
class ObjectNotFound:
    pass


class AuthorStream(APIView):
    permission_classes = [IsAuthenticated]
    http_method_names = ["get"]

    def get(self, request, *args, **kwargs):
        author_id = kwargs['author_id']

        try:
            author = Author.objects.get(_id=author_id, is_active=True)
        except:
            author = None

        if request.user.username != author.user.username:
            author = None

        if not author:
            return HttpResponseNotFound()

        posts_json = list()

        try:
            inbox = Inbox.objects.get(author=author)
        except ObjectNotFound:
            inbox = list()

        inbox = list(inbox.posts.all())

        author_posts = list(Post.objects.all().filter(author=author))

        inbox = inbox + author_posts

        inbox.sort(key=lambda x: x.published, reverse=True)

        followers = list(author.followers.all())

        for post in inbox:
            if post.unlisted:
                continue
            if post.visibility == "FRIENDS" and post.author not in followers:
                continue
            posts_json.append(post.toJSON())

        return HttpResponse(json.dumps(posts_json), content_type=CONTENT_TYPE_JSON)

def encode_list(authors):
    return {
        "type": "author",
        "items": authors
    }


