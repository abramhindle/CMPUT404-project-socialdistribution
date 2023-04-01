from service.models.post import Post
from service.services.team_10.authors import get_or_create_author
from service.services.team_10.helper_constants import HOST
from service.services.remote_helpers import get_author_id, get_remote, post_remote


def get_likes(author, post):
    author_guid = get_author_id(author)
    post_guid = post.source.rsplit('/', 1)[-1]

    url = HOST + "api/authors/" + author_guid + "/posts/" + post_guid + "/likes"

    response = get_remote(url)
    if not response:
        return None

    response_json = response.json()

    print(response_json)

    for like in response_json["items"]:
        like_author = get_or_create_author(like["author"], HOST)
        like["author"] = like_author.toJSON()

    return response_json["items"]


def serialize_like(request, author):
    author_guid = get_author_id(author)
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
        object_guids = request["object"].split('/')
        post_guid = object_guids[-3]
        comment_guid = object_guids[-1]

        object = HOST + "authors/" + author_guid + "/posts/" + post_guid + "/comments/" + comment_guid
        request_json["object"] = object

        request_json["summary"] = f"{request['author']['displayName']} likes your comment"
        request_json["@context"] = "Comment Like"

    print(request_json)

    url = HOST + "api/authors/" + author_guid + "/inbox/"
    response = post_remote(url, request_json)

    return response
