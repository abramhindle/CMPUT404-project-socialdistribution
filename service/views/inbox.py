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


# import requests #TODO: decide if we are ok with using requests to make object creation requests

# flow of endpoints
# -> POST post for {author_id} -> for {follower_author_id} of {author_id} of post (POST Inbox {follower author Id})

@method_decorator(csrf_exempt, name='dispatch')
class InboxView(APIView):
    http_method_names = ["get", "post", "delete"]

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

    def post(self, request: HttpRequest, *args, **kwargs):
        self.author_id = kwargs['author_id']

        # should also go out to the team and get their values
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
            return HttpResponse()

        if author.host == settings.REMOTE_USERS[3][1]:
            response = team_10.handle_inbox(body)
            # if response is None:
            #     return HttpResponseServerError()

            return HttpResponse(status=202)

        try:  # if inbox is empty, it will likely not exist yet, so we need to either get it or instantiate it
            inbox = Inbox.objects.get(author=author) # author_id is the primary key for an inbox
        except ObjectDoesNotExist:
            inbox = Inbox.objects.create(author=author)

        try:
            if body["type"] == "post":
                id = body["id"]
                self.handle_post(inbox, id, body, author, request.user)
            elif body["type"] == "comment":
                id = body["id"]
                self.handle_comment(inbox, id, body, author)
            elif body["type"] == "follow": #TODO: fill these in once the objects are done
                self.handle_follow(inbox, body, author)
            elif body["type"] == "Like":
                id = Like.create_like_id(body["author"]["id"], body["object"])
                self.handle_like(inbox, id, body, author)
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
    
    def handle_post(self, inbox: Inbox, id, body, author, user):
        post = inbox.posts.all().filter(_id=id)

        if post.exists():
            raise ConflictException # conflict, item is already in inbox

        try:
            post = Post.objects.get(_id=id)
        except ObjectDoesNotExist:
            if user.username == "remote-user-t14": #get the post from each DB
                author = team_14.get_or_create_author(body["author"])
                post = team_14.get_or_create_post(body, author, author.host)
            elif user.username == "remote-user-t22":
                author = team_22.get_or_create_author(body["author"])
                post = team_22.get_or_create_post(body, author, author.host)
            elif user.username == "remote-user-t16":
                author = team_16.get_or_create_author(body["author"])
                post = team_16.get_or_create_post(body, author, author.host)

        inbox.posts.add(post)
        inbox.save()

    def handle_comment(self, inbox: Inbox, id, body, author):
        # no idea how to handle this remotely with the spec

        comment = inbox.comments.all().filter(_id=id)

        if comment.exists():
            raise ConflictException # conflict, item is already in inbox

        comment = Comment.objects.get(_id=id)

        inbox.comments.add(comment)
        inbox.save()

#TODO: get or create author from the user
    def handle_follow(self, inbox: Inbox, body, author: Author): # we actually create the follow request here

        if author.host == settings.REMOTE_USERS[0][1]: #get the post from each DB
            foreign_author = team_14.get_or_create_author(body["actor"])
        elif author.host == settings.REMOTE_USERS[1][1]:
            foreign_author = team_22.get_or_create_author(body["actor"])
        elif author.host == settings.REMOTE_USERS[2][1]:
            foreign_author = team_16.get_or_create_author(body["actor"])
        elif author.host == settings.REMOTE_USERS[3][1]:
            foreign_author = team_10.get_or_create_author(body["actor"])
        else:
            print(body["actor"])
            #foreign_author = foreign_author.toObject(body["actor"])
            foreign_author = Author.objects.get(_id=body["actor"]["id"])

        if author._id == foreign_author._id:
            return HttpResponseBadRequest() #can't follow yourself!

        try:
            author.followers.get(_id=foreign_author._id)
            raise ConflictException # request already exists
        except ObjectDoesNotExist:
            r = Follow()
            r._id = Follow.create_follow_id(author._id, foreign_author._id)
            r.actor = foreign_author
            r.object = author
            r.save()

        inbox.follow_requests.add(r)
        inbox.save()

    def handle_like(self, inbox: Inbox, id, body, author: Author):
        like = inbox.likes.all().filter(_id=id)

        if like.exists():
            raise ConflictException

        foreign_author = Author()
        #foreign_author.toObject(body["author"])

        try:
            print(foreign_author._id)
            foreign_author = Author.objects.get(_id=body["author"]["id"], is_active=True)
        except ObjectDoesNotExist:
            print("HERE")
            if author.host == settings.REMOTE_USERS[0][1]:
                #team_14.get_multiple_posts(author)
                pass
            # remote-user-t22
            elif author.host == settings.REMOTE_USERS[1][1]:
                #team_22.get_multiple_posts(author)
                pass
            # remote-user-t16
            elif author.host == settings.REMOTE_USERS[2][1]:
                team_16.get_or_create_author(body["author"])
            elif author.host == settings.REMOTE_USERS[3][1]:
                team_10.get_or_create_author(body["author"])
            else:
                foreign_author.toObject(body["author"])
                foreign_author.save()

        try:
            like = Like.objects.get(_id=id)
        except ObjectDoesNotExist:
            like = Like()
            like._id = id
            like.context = body["context"]

            if(body["object"].split("/")[-2] == "posts"):
                like.summary = f"{foreign_author.displayName} likes your post"
            else:
                like.summary = f"{foreign_author.displayName} likes your comment"
            like.author = foreign_author
            like.object = body["object"]
            like.published
            like.save()

        inbox.likes.add(like)
        inbox.save()


class ConflictException(Exception):
    pass
