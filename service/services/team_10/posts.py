from django.core.exceptions import ObjectDoesNotExist

from service.models.post import Post
from service.services.team_10.helper_constants import HOST
from service.services.remote_helpers import get_author_id, get_remote


def get_or_create_post(post_json, author, hostname=HOST):
    # use source as the id for the remote
    # use origin as the host name
    remote_source = str(post_json["id"])

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


def get_multiple_posts(author):
    author_guid = get_author_id(author)
    url = HOST + "api/authors/" + author_guid + "/posts/"
    response = get_remote(url)

    if not response:
        return None

    items = list()

    for item in response.json()["items"]:  # just returns a list
        post = get_or_create_post(item, author, author.host)
        items.append(post.toJSON())

    return items
