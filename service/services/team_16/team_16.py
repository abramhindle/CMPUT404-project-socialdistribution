from django.core.exceptions import ObjectDoesNotExist

from service.models import Author
from django.conf import settings

import requests

from service.models.post import Post
from service.services.remote_helpers import get_author_id

HOST = settings.REMOTE_USERS[2][1]
AUTH = settings.REMOTE_USERS[2][2]

def get_remote(url):
    try:
        response = requests.get(url, auth=AUTH)
        response.close()
    except Exception as e:
        print("Got an exception of: ", e)
        return None

    if response.status_code < 200 or response.status_code > 299:
        print("Got a status code of: ", response.status_code)
        return None

    return response

# region AUTHOR HELPERS

def get_or_create_author(author_json, hostname):
    try:
        # update old -> don't change host_url or id
        old_author = Author.objects.get(url=author_json["id"])

        old_author.github = author_json["github"]
        old_author.displayName = author_json["displayName"]
        old_author.url = author_json["id"]
        old_author.save()

        return old_author

    except ObjectDoesNotExist:
        # create new author
        new_author = Author()
        new_author.github = author_json["github"]
        new_author.displayName = author_json["displayName"]
        new_author.url = author_json["id"]
        new_author.host = hostname
        new_author.save()

        return new_author

def get_single_author(author):
    author_guid = get_author_id(author)
    url = HOST + "service/authors/" + author_guid
    response = get_remote(url)

    if not response:
        return None

    return get_or_create_author(response.json(), HOST)

def get_multiple_authors(page, size):
    url = HOST + "service/authors/"
    response = get_remote(url)

    if not response:
        return

    response_json = response.json()

    for author in response_json["items"]:
        get_or_create_author(author, HOST)

# endregion

# region POST HELPERS


def get_or_create_post(post_json, author, hostname):
    # use source as the id for the remote
    # use origin as the host name
    remote_source = hostname + str(post_json["id"])  # this is an int

    try:
        # update old -> don't change host_url or id
        old_post = Post.objects.get(source=remote_source)
        old_post = post_to_object(old_post, post_json)
        old_post.save()

        return old_post

    except ObjectDoesNotExist:
        # create new
        new_post = post_to_object(Post(), post_json)
        new_post._id = Post.create_post_id(author._id)
        new_post.source = remote_source
        new_post.author = author
        new_post.origin = hostname
        new_post.save()

        return new_post

def get_multiple_posts(author, page, size):
    author_guid = get_author_id(author)

    url = HOST + "service/authors/" + author_guid + "/posts/"

    response = get_remote(url)

    if not response:
        return None

    items = list()

    print(response.json())

    for item in response.json()["items"]:  # just returns a list
        print(item)
        post = get_or_create_post(item, author, HOST)
        items.append(post.toJSON())

    return items

def post_to_object(post, json_object):
    post.title = json_object["title"]
    post.source = json_object["source"]
    post.description = json_object["description"]
    post.contentType = json_object["contentType"]
    post.content = json_object["content"]
    post.published = json_object["published"]
    post.visibility = json_object["visibility"]
    post.unlisted = bool(json_object["unlisted"])
    return post

# endregion

# region FOLLOWER HELPERS

def get_followers(author):
    author_guid = get_author_id(author)
    url = HOST + "service/authors/" + author_guid + "/followers"
    response = get_remote(url)

    if not response:
        return None

    response_json = response.json()

    authors = list()

    for follower in response_json["items"]:
        follower = get_or_create_author(follower, HOST)
        author.followers.add(follower)
        authors.append(follower.toJSON())

    author.save()

    return authors

def serialize_follow_request(request):
    author_guid = request["object"]["url"].rsplit('/', 1)[-1]
    print(author_guid)
    url = HOST + "service/authors/" + author_guid
    response = get_remote(url)

    if not response:
        return None

    author = response.json()

    request["actor"]["type"] = "author"
    request["actor"].pop("isLogin")

    json_request = {
        "type": "Follow",
        "summary": request["Summary"],
        "actor": request["actor"], #our own author
        "object": author
    }

    url = HOST + "service/authors/" + author_guid + "/inbox/"
    try:  # try get Author
        response = requests.post(url, json=json_request, auth=AUTH)
        response.close()
    except Exception as e:
        print(e)
        return None

    if response.status_code < 200 or response.status_code > 299:
        print(response.status_code)
        author = None
        return author

    return response

def serialize_post(request, author):
    author_guid = author.url.rsplit('/', 1)[-1]
    print(author_guid)

    #request["comments"] = request["id"] + "/comments/"
    if request["visibility"] == "PUBLIC":
        request["visibility"] = "VISIBLE"
    request["count"] = 0

    #request["categories"] = ", ".join(request["categories"])
    request["source"] = settings.DOMAIN
    request["origin"] = settings.DOMAIN

    print(request)

    url = HOST + "service/authors/" + author_guid + "/inbox/"
    try:  # try get Author
        print(url)
        response = requests.post(url, json=request, auth=AUTH)
        response.close()
    except Exception as e:
        print(e)
        return None  # just say not found

    if response.status_code < 200 or response.status_code > 299:
        print(response.status_code)
        print(response.text)
        return None

    print(response.status_code)

    return response

# endregion

def handle_inbox(body, author):
    response = None
    if body["type"] == "post":
        response = serialize_post(body, author)
    elif body["type"] == "comment":
        #self.handle_comment(inbox, id, body, author)
        pass
    elif body["type"] == "follow":
        response = serialize_follow_request(body)
    elif body["type"] == "Like":
        pass
        #id = Like.create_like_id(body["author"]["id"], body["object"])

    return response