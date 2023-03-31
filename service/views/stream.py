import json

from django.http import *
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from service.models.author import Author
from service.models.post import Post
from service.service_constants import *

#returns an author's stream
class AuthorStream(APIView):
    permission_classes = [IsAuthenticated]
    http_method_names = ["get"]

    def get(self, request, *args, **kwargs):
        author_id = kwargs['author_id']
        # rework this so it goes out, gets all posts from other servers, then puts them in a list
        try:
            author = Author.objects.get(_id=author_id, is_active=True)
        except:
            author = None

        if request.user.username != author.user.username:
            author = None

        if not author:
            return HttpResponseNotFound()

        #get list of following
        following = Author.objects.all().filter(followers___id__contains=author._id)

        posts_json = list()

        #needs visibility filtering.
        posts = Post.objects.all().filter(author__in=following).order_by('-published')

        for post in list(posts):
            posts_json.append(post.toJSON())

        return HttpResponse(json.dumps(posts_json), content_type=CONTENT_TYPE_JSON)

def encode_list(authors):
    return {
        "type": "author",
        "items": authors
    }


