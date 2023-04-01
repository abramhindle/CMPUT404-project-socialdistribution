from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
from django.conf import settings
from django.http import *
import json
from datetime import datetime, timezone

from django.core.exceptions import ObjectDoesNotExist
from rest_framework.views import APIView

from service.models.author import Author
from service.models.comment import Comment
from service.models.post import Post
from service.service_constants import *

from rest_framework.permissions import IsAuthenticated

from service.services import team_14, team_22, team_16
import service.services.team_10.comments as team_10
import service.services.team_16.team_16 as team_16


@method_decorator(csrf_exempt, name='dispatch')
class CommentView(APIView):
    permission_classes = [IsAuthenticated]
    http_method_names = ["get", "post"]
    def get(self, request, *args, **kwargs):
        """ Get a list of comments for a post """
        self.author_id = kwargs['author_id']
        self.post_id = kwargs['post_id']

        try:
            author = Author.objects.get(_id=self.author_id)
        except ObjectDoesNotExist:
            return HttpResponseNotFound()

        try:
            post = Post.objects.get(_id=self.post_id)
        except ObjectDoesNotExist:
            return HttpResponseNotFound()

        comments_json = list()

        if post.origin == settings.REMOTE_USERS[0][1]:
            #team_14.get_multiple_posts(author)
            pass
        # remote-user-t22
        elif post.origin == settings.REMOTE_USERS[1][1]:
            #team_22.get_multiple_posts(author)
            pass
        # remote-user-t16
        elif post.origin == settings.REMOTE_USERS[2][1]:
            comments_json = team_16.get_comments(author, post)
        # team 10
        elif post.origin == settings.REMOTE_USERS[3][1]:
            comments_json = team_10.get_comments(author, post)
        else:
            comments_json = self.get_local_comments(request)

        return HttpResponse(json.dumps(comments_json), content_type = CONTENT_TYPE_JSON)

    def get_local_comments(self, request):
        """ Goes to the DB and retrieves a paged list of comments"""
        comments = list()

        page = request.GET.get('page', 1)
        size = request.GET.get('size', 5)
        comment_queryset = Comment.objects.all().filter(post=self.post_id).order_by('-published')
        host = request.build_absolute_uri('/')  # gets the base of the host -> http://localhost:8000
        paged_comments = Paginator(comment_queryset, size)
        try:
            comment_page = paged_comments.page(page)  # default to page 1
        except:
            comment_page = list()
        for comment in comment_page:
            comments.append(comment.toJSON())
        comments_json = encode_list(comments, host, page, size, self.author_id, self.post_id)
        return comments_json

    ### POST
    def post(self, request, *args, **kwargs):
        """ Creates a comment for the given post """
        self.author_id = kwargs['author_id']
        self.post_id = kwargs['post_id']

        try:
            post = Post.objects.get(_id=self.post_id)
            author = Author.objects.get(_id=self.author_id, is_active=True)
        except ObjectDoesNotExist:
            return HttpResponseNotFound()

        try:
            body = request.data
        except AttributeError:  # tests don't run without this
            body = request.body
            body = json.loads(body)

        comment = Comment()

        try:
            comment._id = Comment.create_comment_id(self.author_id, self.post_id)
            comment.comment = body["comment"]
            comment.author = author
            comment.post = post

            is_valid = False
            if (body["contentType"] in ("text/markdown", "text/plain")):
                is_valid = True

            if not is_valid:
                return HttpResponseBadRequest()

            comment.contentType = body["contentType"]
            comment.published = datetime.now(timezone.utc)

        except KeyError:
            return HttpResponseBadRequest()

        comment.save()

        comment_json = comment.toJSON()

        return HttpResponse(json.dumps(comment_json), status=201, content_type = CONTENT_TYPE_JSON)

def encode_list(comments, host, page, size, author_id, post_id):
    """ Returns the proper format for a list of comments """
    return {
        "type": "comments",
        "page": int(page),
        "size": int(size),
        "post": f"{host}authors/{author_id}/posts/{post_id}",
        "id": f"{host}authors/{author_id}/posts/{post_id}/comments",
        "items": comments
    }