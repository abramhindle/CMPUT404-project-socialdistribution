from django.conf import settings

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


def handle_inbox(body, author):
    response = None
    if body["type"] == "post":
        response = serialize_post(body, author)
    elif body["type"] == "comment":
        # self.handle_comment(inbox, id, body, author)
        pass
    elif body["type"] == "follow":
        response = serialize_follow_request(body)
    elif body["type"] == "Like":
        response = serialize_like(body, author)

    return response