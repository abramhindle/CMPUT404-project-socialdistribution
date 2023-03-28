import json

from django.core.exceptions import ObjectDoesNotExist

from service.models import Author
from django.conf import settings

import requests

from service.models.post import Post


AUTH = {'Authorization': 'Token ' + settings.REMOTE_USERS[3][2]}
HOST = settings.REMOTE_USERS[3][1]

# AUTHOR HELPERS

def get_or_create_author(author_json, hostname):
    try:
        # update old -> don't change host_url or id
        old_author = Author.objects.get(url=author_json["url"])

        old_author.github = author_json["github"]
        old_author.displayName = author_json["displayName"]
        old_author.save()

        return old_author

    except ObjectDoesNotExist:
        # create new
        new_author = Author()
        new_author._id = f"{settings.DOMAIN}/authors/{author_json['id']}"  # we use the GUID sent to us
        new_author.github = author_json["github"]
        new_author.displayName = author_json["displayName"]
        new_author.url = author_json["url"]
        new_author.host = hostname
        new_author.save()

        return new_author

def get_single_author(author):
    author_guid = author.url.rsplit('/', 2)[-2]
    try:
        response = requests.get(HOST + "service/authors/" + author_guid + "/",
                                headers=AUTH)
        response.close()
    except:
        return None

    if response.status_code < 200 or response.status_code > 299:
        author = None
        return author

    return get_or_create_author(response.json(), author.host)

def get_multiple_authors(page, size):
    try:
        response = requests.get(HOST + "api/authors/", headers=AUTH)
        response.close()
    except Exception as e:
        return

    if response.status_code < 200 or response.status_code > 299:  # unsuccessful
        print(response.status_code)
        return

    response_json = response.json()

    for author in response_json["items"]:
        #print(author)
        get_or_create_author(author, HOST)

# POST HELPERS

def get_multiple_posts(author):
    url = HOST + "service/authors/" + author.url.rsplit('/', 2)[-2] + "/posts/"

    try:
        response = requests.get(url, headers=AUTH)
        response.close()
    except:
        return

    if response.status_code < 200 or response.status_code > 299:  # unsuccessful
        return

    items = list()

    for item in response.json():  # just returns a list
        post = get_or_create_post(item, author, author.host)
        items.append(post.toJSON())

    return items

def get_or_create_post(post_json, author, hostname):
    # use source as the id for the remote
    # use origin as the host name
    remote_source = hostname + str(post_json["id"])  # this is an int

    try:
        # update old -> don't change host_url or id
        old_post = Post.objects.get(source=remote_source)
        return old_post

    except ObjectDoesNotExist:
        # create new
        new_post = post_to_object(Post(), post_json, author)
        new_post._id = Post.create_post_id(author._id)
        new_post.source = remote_source
        new_post.author = author
        new_post.origin = hostname
        new_post.save()

        return new_post

def post_to_object(post, json_object, author):
    post.title = json_object["title"]
    post.source = json_object["source"]
    post.description = json_object["description"]
    post.contentType = json_object["content_type"]
    post.content = json_object["content"]
    post.author = author
    post.published = json_object["published"]
    post.visibility = json_object["visibility"]
    post.unlisted = bool(json_object["unlisted"])
    return post

def serialize_follow_request(request):
    author_guid = request["object"]["url"].rsplit('/', 2)[-2]
    try:
        response = requests.get(HOST + "service/authors/" + author_guid + "/",
                                headers={'Authorization': 'Basic ' + settings.REMOTE_USERS[1][2]})
        response.close()
    except:
        return None

    author = response.json()

    if response.status_code < 200 or response.status_code > 299:
        author = None
        return author

    request["actor"]["type"] = "author"

    json_request = {
        "type": "Follow",
        "summary": request["Summary"],
        "actor": request["actor"], #our own author
        "object": author
    }

    url = HOST + "service/authors/" + author_guid + "/inbox/"
    try:  # try get Author
        response = requests.post(url, json=json_request, headers={'Authorization': 'Basic ' + settings.REMOTE_USERS[1][2]})
        response.close()
    except Exception as e:
        print(e)
        return None  # just say not found

    print(response.status_code)
    print(response.json())
    return response

def serialize_post(request):
    author_guid = request["object"]["url"].rsplit('/', 2)[-2]
    try:
        response = requests.get(HOST + "service/authors/" + author_guid + "/",
                                headers={'Authorization': 'Basic ' + settings.REMOTE_USERS[1][2]})
        response.close()
    except:
        return None

    author = response.json()

    if response.status_code < 200 or response.status_code > 299:
        author = None
        return author

    request["actor"]["type"] = "author"

    json_request = {
        "type": "Follow",
        "summary": request["Summary"],
        "actor": request["actor"], #our own author
        "object": author
    }

    url = HOST + "service/authors/" + author_guid + "/inbox/"
    try:  # try get Author
        response = requests.post(url, json=json_request, headers={'Authorization': 'Basic ' + settings.REMOTE_USERS[1][2]})
        response.close()
    except Exception as e:
        print(e)
        return None  # just say not found

    print(response.status_code)
    print(response.json())
    return response

def handle_inbox(body):
    response = None
    if body["type"] == "post":
        pass
        #self.handle_post(inbox, id, body, author, request.user)
    elif body["type"] == "comment":
        #self.handle_comment(inbox, id, body, author)
        pass
    elif body["type"] == "follow":
        response = serialize_follow_request(body)
    elif body["type"] == "Like":
        pass
        #id = Like.create_like_id(body["author"]["id"], body["object"])

    return response