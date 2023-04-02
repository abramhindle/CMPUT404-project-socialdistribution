from django.conf import settings

from service.models.post import Post
from service.services.team_10.authors import get_multiple_authors
from service.services.team_10.helper_constants import HOST
from service.services.remote_helpers import get_author_id, get_remote, post_remote
from service.services.team_10.likes import serialize_like


def serialize_follow_request(request):
    """ Creates a follow request and POSTs it to team_10 """
    author_guid = request["object"]["url"].rsplit('/', 1)[-1]

    url = HOST + "api/authors/" + author_guid + "/"
    response = get_remote(url)
    if not response:
        return None

    author = response.json()

    request["actor"]["type"] = "author"

    json_request = {
        "type": "Follow",
        "summary": request["Summary"],
        "actor": request["actor"],  # our own author
        "object": author
    }

    url = HOST + "api/authors/" + author_guid + "/inbox/"
    response = post_remote(url, json_request)
    return response


def serialize_post(request, author):
    """ Creates a post and POSTs it to team_10 """
    author_guid = get_author_id(author)

    request["comments"] = request["id"] + "/comments/"
    if request["visibility"] == "PUBLIC":
        request["visibility"] = "VISIBLE"
    request["count"] = 0

    if request["contentType"] == "image/jpeg":
        request["contentType"] = "image/jpeg;base64"
    elif request["contentType"] == "image/png":
        request["contentType"] = "image/png;base64"

    request["categories"] = ", ".join(request["categories"])
    request["source"] = settings.DOMAIN
    request["origin"] = settings.DOMAIN

    print(request)

    url = HOST + "api/authors/" + author_guid + "/inbox/"
    response = post_remote(url, request)

    return response

def serialize_comment(request, author):
    """ Creates a post and POSTs it to team_10 """
    # author id in request id will always be our own
    # post id in request id should be the remote
    # comment id should be our own
    author_guid = get_author_id(author)
    comment_guid = request["id"].rsplit('/', 1)[-1]

    request_json = {
        "type": "comment",
        "author": request["author"], #always a local author
        "content": request["comment"],
        "contentType": request["contentType"],
        "published": request["published"],
    }

    local_post_guid = request["id"].rsplit('/', 2)[0]

    post = Post.objects.get(_id=local_post_guid)
    post_guid = post.source.rsplit('/', 1)[-1] #remote post guid

    request_json["id"] = HOST + "authors/" + author_guid + "/posts/" + post_guid + "/comments/" + comment_guid
    url = HOST + "api/authors/" + author_guid + "/inbox/"
    response = post_remote(url, request_json)

    return response


def handle_inbox(body, author):
    response = None
    if body["type"] == "post":
        response = serialize_post(body, author)
    elif body["type"] == "comment":
        response = serialize_comment(body, author)
    elif body["type"] == "follow":
        response = serialize_follow_request(body)
    elif body["type"] == "Like":
        response = serialize_like(body, author)

    return response