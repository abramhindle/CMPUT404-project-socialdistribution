from datetime import datetime, timezone

from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseBadRequest

from service.models import Author, Comment
from service.models.follow import Follow
from service.models.inbox import Inbox
from django.conf import settings

from service.models.like import Like
from service.models.post import Post
from service.services import team_16, team_14, team_22

from service.services.team_10 import authors as team_10_authors, posts as team_10_posts



def handle_comment(inbox: Inbox, body, author):

    if body["author"]["host"] == settings.REMOTE_USERS[0][1]:  # get the author from remote hosts
        author = team_14.get_or_create_author(body["author"])
    elif body["author"]["host"] == settings.REMOTE_USERS[1][1]:
        author = team_22.get_or_create_author(body["author"])
    elif body["author"]["host"] == settings.REMOTE_USERS[2][1]:
        author = team_16.get_or_create_author(body["author"])
    elif body["author"]["host"] == settings.REMOTE_USERS[3][1]:
        author = team_10_authors.get_or_create_author(body["author"])
    else:
        author = Author.objects.get(_id=body["author"]["id"], is_active=True)

    id = body["id"]

    comment = inbox.comments.all().filter(_id=id)

    if comment.exists():
        raise ConflictException  # conflict, item is already in inbox

    try:
        comment = Comment.objects.get(_id=id)
    except ObjectDoesNotExist:
        post = Post.objects.get(_id=id)  # if they only pass us a post id, we assume they are creating
        comment = Comment()
        comment._id = Comment.create_comment_id(author._id, post._id)
        comment.comment = body["comment"]
        comment.author = author
        comment.post = post

        is_valid = False
        if (body["contentType"] in ("text/markdown", "text/plain")):
            is_valid = True

        if not is_valid:
            raise KeyError

        comment.contentType = body["contentType"]
        comment.published = datetime.now(timezone.utc)

    inbox.comments.add(comment)
    inbox.save()

def handle_post(inbox: Inbox, id, body, author, user):
    print(body)
    if body["author"]["host"] == settings.REMOTE_USERS[0][1]:  # get the author from remote hosts
        author = team_14.get_or_create_author(body["author"])
        post = team_14.get_or_create_post(body, author, author.host)
        post_id = post._id
    elif body["author"]["host"] == settings.REMOTE_USERS[1][1]:
        author = team_22.get_or_create_author(body["author"])
        post = team_22.get_or_create_post(body, author, author.host)
        post_id = post._id
    elif body["author"]["host"] == settings.REMOTE_USERS[2][1]:
        author = team_16.get_or_create_author(body["author"])
        post = team_16.get_or_create_post(body, author, author.host)
        post_id = post._id
    elif body["author"]["host"] == settings.REMOTE_USERS[3][1]:
        author = team_10_authors.get_or_create_author(body["author"])
        post = team_10_posts.get_or_create_post(body, author)
        post_id = post._id
    else:
        author = Author.objects.get(_id=body["author"]["id"], is_active=True)
        post_id = body["id"]

    post = Post.objects.get(_id=post_id)

    inbox_post = inbox.posts.all().filter(_id=post._id)

    if inbox_post.exists():
        raise ConflictException  # conflict, item is already in inbox

    inbox.posts.add(post)
    inbox.save()


def handle_follow(inbox: Inbox, body, author: Author):  # we actually create the follow request here
    print("BODY")
    print(body)
    print()

    #print(body["actor"]["host"])
    #print(settings.REMOTE_USERS[3][1])

    if body["actor"]["host"] == settings.REMOTE_USERS[0][1]:  # get the author from remote hosts
        foreign_author = team_14.get_or_create_author(body["actor"])
    elif body["actor"]["host"] == settings.REMOTE_USERS[1][1]:
        foreign_author = team_22.get_or_create_author(body["actor"])
    elif body["actor"]["host"] == settings.REMOTE_USERS[2][1]:
        foreign_author = team_16.get_or_create_author(body["actor"])
    elif body["actor"]["host"] == settings.REMOTE_USERS[3][1]:
        foreign_author = team_10_authors.get_or_create_author(body["actor"])
    else:
        foreign_author = Author.objects.get(_id=body["actor"]["id"])

    if author._id == foreign_author._id:
        return HttpResponseBadRequest()  # can't follow yourself!

    try:
        author.followers.get(_id=foreign_author._id)
        raise ConflictException  # request already exists
    except ObjectDoesNotExist:
        r = Follow()
        r._id = Follow.create_follow_id(author._id, foreign_author._id)
        r.actor = foreign_author
        r.object = author
        r.save()

    inbox.follow_requests.add(r)
    inbox.save()

def handle_like(inbox: Inbox, body, author: Author):
    foreign_author = Author()

    # check if author is remote
    if body["author"]["host"] == settings.REMOTE_USERS[0][1]:
        # team_14.get_multiple_posts(author)
        pass
    # remote-user-t22
    elif body["author"]["host"] == settings.REMOTE_USERS[1][1]:
        # team_22.get_multiple_posts(author)
        pass
    # remote-user-t16
    elif body["author"]["host"] == settings.REMOTE_USERS[2][1]:
        foreign_author = team_16.get_or_create_author(body["author"])
    elif body["author"]["host"] == settings.REMOTE_USERS[3][1]:
        foreign_author = team_10_authors.get_or_create_author(body["author"])
    else: # otherwise get it from DB
        foreign_author = Author.objects.get(_id=body["author"]["id"], is_active=True)

    id = Like.create_like_id(foreign_author._id, body["object"])

    like = inbox.likes.all().filter(_id=id)

    if like.exists():
        raise ConflictException

    try:
        like = Like.objects.get(_id=id)
    except ObjectDoesNotExist:
        like = Like()
        like._id = id
        try:
            like.context = body["context"]
        except:
            like.context = body["@context"]

        if(body["object"].split("/")[-2] == "posts"):
            like.summary = f"{foreign_author.displayName} likes your post"
        else:
            like.summary = f"{foreign_author.displayName} likes your comment"
        like.author = foreign_author
        like.object = body["object"]
        like.save()

    inbox.likes.add(like)
    inbox.save()

class ConflictException(Exception):
    pass