import requests
from urllib.parse import urljoin
from requests.auth import HTTPBasicAuth
from requests.exceptions import Timeout
from servers.models import Server


PUBLIC_POSTS_ENDPOINT = "posts/"
CONNECTION_TIMEOUT_LIMIT = 10
READ_TIMEOUT_LIMIT = 20

AUTHOR_FIELDS = ["id", "host", "displayName", "url", "github"]
COMMENT_FIELDS = ["author", "comment", "contentType", "published", "id"]
POST_FIELDS = ["title", "source", "origin", "description", "contentType",
               "author", "categories", "count", "size", "next", "comments",
               "published", "id", "visibility", "visibleTo", "unlisted"]



def validate_instance(instance, fields, type):
    if not isinstance(instance, dict):
        print("instance not a dictionary")
        return False
    for field in fields:
        if field not in instance:
            print("%s not in %s" % (field, type))
            return False
    return True


def validate_remote_post_response(post):

    if (not validate_instance(post, POST_FIELDS, "post")
            or not validate_instance(post.get("author"), AUTHOR_FIELDS, "author")):
        return False

    comments = post.get("comments")

    for comment in comments:

        if (not validate_instance(comment, COMMENT_FIELDS, "comment")
                or not validate_instance(comment.get("author"), AUTHOR_FIELDS, "author")):
            return False

    return True


def get_api_request_url(server_api, server_endpoint):
    return urljoin(server_api, server_endpoint)


def get_public_posts_from_remote_server(server):

    server_api_location = server.api_location
    server_user = server.remote_server_user
    server_pass = server.remote_server_pass

    api_request_url = get_api_request_url(server_api_location,
                                          PUBLIC_POSTS_ENDPOINT)

    try:
        response = requests.get(
            api_request_url,
            auth=HTTPBasicAuth(server_user, server_pass),
            timeout=(CONNECTION_TIMEOUT_LIMIT, READ_TIMEOUT_LIMIT)
        )

        if response.status_code != 200:
            print("%s - unable to complete request." % (response.status_code))
            return None

        server_posts = response.json().get("posts", None)

        if not server_posts:
            print("Received a malformed response from %s." % (api_request_url))
            return None

        post_instances = []
        for post in server_posts:
            # This should not be done on the server end
            # We should be sending json response to front-end and verify there
            if not validate_remote_post_response(post):
                print("Malformed post. Ignoring ...")
                # continue
            post_instances.append(post)

        return post_instances

    except Timeout:
        print("Request to %s timed out." % (api_request_url))
        return None
    except Exception as error:
        print("Unknown error: %s." % (error))
        return None


def get_public_posts_from_remote_servers():
    servers = Server.objects.all()
    posts = []
    for server in servers:
        server_posts = get_public_posts_from_remote_server(server)
        if server_posts:
            for post in server_posts:
                posts.append(post)

    return posts
