import json

from django.core.exceptions import ObjectDoesNotExist

from service.models import Author, Comment
from django.conf import settings

import requests

from service.models.post import Post


AUTH = {'Authorization': 'Token ' + settings.REMOTE_USERS[3][2]}
HOST = settings.REMOTE_USERS[3][1]

# AUTHOR HELPERS

def get_or_create_author(author_json, hostname=HOST):
    try:
        # update old -> don't change host_url or id
        old_author = Author.objects.get(url=author_json["id"])

        old_author.github = author_json["github"]
        old_author.displayName = author_json["displayName"]
        old_author.save()

        return old_author

    except ObjectDoesNotExist:
        # create new
        new_author = Author()
        #new_author._id = f"{settings.DOMAIN}/authors/{author_json['id']}"  # we use the GUID sent to us
        new_author.github = author_json["github"]
        new_author.displayName = author_json["displayName"]
        new_author.url = author_json["id"]
        new_author.host = hostname
        new_author.save()

        return new_author

def get_single_author(author):
    author_guid = author.url.rsplit('/', 1)[-1]
    try:
        response = requests.get(HOST + "api/authors/" + author_guid,
                                headers=AUTH)
        response.close()
    except:
        return None

    if response.status_code < 200 or response.status_code > 299:
        author = None
        return author

    return get_or_create_author(response.json(), author.host)

def get_multiple_authors(page, size): #no paging yet
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
        get_or_create_author(author, HOST)

# POST HELPERS

def get_multiple_posts(author):
    url = HOST + "api/authors/" + author.url.rsplit('/', 1)[-1] + "/posts/"

    try:
        response = requests.get(url, headers=AUTH)
        response.close()
    except Exception as e:
        print(e)
        return

    if response.status_code < 200 or response.status_code > 299:  # unsuccessful
        print(response.status_code)
        return

    items = list()

    for item in response.json()["items"]:  # just returns a list
        post = get_or_create_post(item, author, author.host)
        items.append(post.toJSON())

    return items

def get_or_create_post(post_json, author, hostname=HOST):
    # use source as the id for the remote
    # use origin as the host name
    remote_source = str(post_json["id"])  # this is an int
    print(remote_source)

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
    post.contentType = json_object["contentType"]
    post.content = json_object["content"]
    post.author = author
    post.published = json_object["published"]
    if json_object["visibility"] == "VISIBLE":
        post.visibility = "PUBLIC"
    else:
        post.visibility = "FRIENDS"

    post.unlisted = bool(json_object["unlisted"])
    return post

def serialize_follow_request(request):
    author_guid = request["object"]["url"].rsplit('/', 1)[-1]
    try:
        response = requests.get(HOST + "api/authors/" + author_guid + "/",
                                headers=AUTH)
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

    print(json_request)

    url = HOST + "api/authors/" + author_guid + "/inbox/"
    try:
        pass
        response = requests.post(url, json=json_request, headers=AUTH)
        response.close()
    except Exception as e:
        print(e)
        return None  # just say not found

    print(response.status_code)
    #print(response.json())
    return response

def serialize_post(request, author):
    author_guid = author.url.rsplit('/', 1)[-1]
    print(author_guid)

    request["comments"] = request["id"] + "/comments/"
    if request["visibility"] == "PUBLIC":
        request["visibility"] = "VISIBLE"
    request["count"] = 0

    request["categories"] = ", ".join(request["categories"])
    request["source"] = settings.DOMAIN
    request["origin"] = settings.DOMAIN

    print(request)

    url = HOST + "api/authors/" + author_guid + "/inbox/"
    try:  # try get Author
        print(url)
        response = requests.post(url, json=request, headers=AUTH)
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

def serialize_like(request, author):
    author_guid = author.url.rsplit('/', 1)[-1]
    object_id = request["object"].rsplit('/', 1)[-1]

    request_json = {
        "type": "Like",
        "author": request["author"],
    }

    if request["object"].split("/")[-2] == "posts":
        local_post_guid = author._id + "/posts/" + object_id

        post = Post.objects.get(_id=local_post_guid)
        post_guid = post.source.rsplit('/', 1)[-1]

        request_json["summary"] = f"{request['author']['displayName']} likes your post"
        request_json["object"] = HOST + "authors/" + author_guid + "/posts/" + post_guid
        request_json["@context"] = "Post Like"
    else:
        print(request)
        post_guid = request_json["object"].split('/')
        print(post_guid[-2])
        request_json["summary"] = f"{request['author']['displayName']} likes your comment"
        request_json["object"] = request["object"]

        request_json["@context"] = "Comment Like"

    print(request_json)

    url = HOST + "api/authors/" + author_guid + "/inbox/"
    try:  # try get Author
        print(url)
        #response = requests.post(url, json=request_json, headers=AUTH)
        #response.close()
    except Exception as e:
        print(e)
        return None  # just say not found

    if response.status_code < 200 or response.status_code > 299:
        print(response.status_code)
        print(response.text)
        return None

    print(response.status_code)

    return response

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
        response = serialize_like(body, author)

    return response

def get_followers(author):
    author_guid = author.url.rsplit('/', 1)[-1]
    try:
        response = requests.get(HOST + "api/authors/" + author_guid + "/followers/",
                                headers=AUTH)
        response.close()
    except:
        return None

    if response.status_code < 200 or response.status_code > 299:
        print(response.status_code)
        return None

    response_json = response.json()
    authors = list()

    for follower in response_json["items"]:
        follower = get_or_create_author(follower, HOST)
        author.followers.add(follower)
        authors.append(follower.toJSON())

    author.save()

    return authors

def get_likes(author, post):
    pass

def get_comments(author, post):
    author_guid = author.url.rsplit('/', 1)[-1]
    post_guid = post.source.rsplit('/', 1)[-1]

    try:
        response = requests.get(HOST + "api/authors/" + author_guid + "/posts/" + post_guid + "/comments/",
                                headers=AUTH)
        response.close()
    except:
        return None

    if response.status_code < 200 or response.status_code > 299:
        print(response.status_code)
        return None

    response_json = response.json()

    response_json["items"] = response_json.pop("items")

    # we CANNOT Store copies of their comments -> no way to differentiate, only one ID field
    for comment in response_json["items"]:
        comment["author"] = author.toJSON()
        comment["comment"] = comment.pop("content")
        print(json.dumps(comment))

    print(response_json)

    return response_json




