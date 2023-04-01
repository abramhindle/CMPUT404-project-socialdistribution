import json

from django.db.models import Q
from django.http import *
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from service.models.author import Author
from service.models.post import Post
from service.service_constants import *
from service.views.post import filter_posts


#returns an author's stream
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

        #get list of following
        following = Author.objects.all().filter(followers___id__contains=author._id)
        posts_json = list()

        #needs visibility filtering.
        posts = Post.objects.all().filter(Q(author__in=following) | Q(author___id=author_id)).order_by('-published')

        #posts = filter_posts(author, posts, author)

        for post in list(posts):
            if post.unlisted:
                continue
            if post.author != author and not is_friend(post.author, author):
                continue
            posts_json.append(post.toJSON())

        return HttpResponse(json.dumps(posts_json), content_type=CONTENT_TYPE_JSON)

def is_friend(author1: Author, author2: Author):
    return author1 in list(author2.followers.all()) and author2 in list(author1.followers.all())

def encode_list(authors):
    return {
        "type": "author",
        "items": authors
    }


