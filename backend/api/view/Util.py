from urllib.parse import urlparse

from django.core.paginator import Paginator
from rest_framework.response import Response
from ..models import AuthorProfile, Follow, Post, Comment, ServerUser
from ..serializers import AuthorProfileSerializer, CommentSerializer, PostSerializer
from ..models import AuthorProfile, Follow, ServerUser
import urllib
from django.conf import settings
import requests
import json


def get_author_id(author_profile, escaped):
    formated_id = AuthorProfileSerializer(author_profile).data["id"]
    if (escaped):
        formated_id = urllib.parse.quote(formated_id, safe='~()*!.\'')
    return formated_id


# the post argument should be a serialized post object
# the friends_list argument should be a list of author id
def can_read(requesting_author_id, post, friends_list):
    try:
        parsed_url = urlparse(requesting_author_id)
        requesting_author_host = '{}://{}/'.format(parsed_url.scheme, parsed_url.netloc)

        if (post["unlisted"]):
            return False

        elif (requesting_author_id == post["author"]["id"] or post["visibility"] == "PUBLIC"):
            return True

        else:
            # check FOAF
            if (post["visibility"] == "FOAF"):
                # check if the author of the post is friends with the requester
                is_friend_filter = Follow.objects.filter(authorA=post["author"]["id"],
                                                         authorB=requesting_author_id,
                                                         status="FRIENDS")
                # they are direct friends
                if (is_friend_filter.exists()):
                    return True
                else:
                    for friend in friends_list:
                        # check if the author of the post is friends with the friends of the requester
                        is_friend_filter = Follow.objects.filter(authorA=friend,
                                                                 authorB=post["author"]["id"],
                                                                 status="FRIENDS")
                        if (is_friend_filter.exists()):
                            return True

                    return False
            # check FRIENDS
            elif (post["visibility"] == "FRIENDS"):
                is_friend_filter = Follow.objects.filter(authorA=post["author"]["id"],
                                                         authorB=requesting_author_id,
                                                         status="FRIENDS")
                if (is_friend_filter.exists()):
                    return True
                else:
                    return False
            # check PRIVATE
            elif (post["visibility"] == "PRIVATE"):
                if (requesting_author_id in post["visibleTo"]):
                    return True
                else:
                    return False
            # check SERVERONLY
            elif (post["visibility"] == "SERVERONLY"):
                if (requesting_author_host == settings.BACKEND_URL):
                    return True
                else:
                    return False
            else:
                return False
    except:
        return False
    return True


def get_author_profile_uuid(author_id):
    unquoted_parse = urllib.parse.unquote(author_id)
    if ("author/" in unquoted_parse):
        author_data = unquoted_parse.split("author/")
        return author_data[1]
    else:
        return None


# assume there is no friends when the request fails, so return empty friends list
def get_foreign_friend_list(author_id):
    try:
        parsed_url = urlparse(author_id)
        author_host = '{}://{}/'.format(parsed_url.scheme, parsed_url.netloc)
        server_user = ServerUser.objects.get(host=author_host)
        author_short_id = author_id.split("author/")[-1]
        url = "{}{}author/{}/friends/".format(server_user.host, server_user.prefix, author_short_id)
        headers = {'Content-type': 'application/json'}
        response = requests.get(url,
                                auth=(server_user.send_username, server_user.send_password),
                                headers=headers)
        friends_list = response.json()["authors"]
        return friends_list
    except:
        return []


def get_local_friends_list(author_id):
    friends_list = Follow.objects.filter(authorA=author_id, status="FRIENDS")
    response_authors = []

    for friend in friends_list:
        response_authors.append(friend.authorB)
    return response_authors


def validate_uuid(author_id):
    try:
        uuid.UUID(author_id)
        return True
    except:
        return False


# posts is a list of post
# author full id includes the id
# is own posts
def build_post(post):
    comments = []
    if ("comments" in post):
        # do stuff
        for comment in post["comments"]:
            # full_author_id = comment["author"] # http://localhost:8000/author/adfhadifnads
            parsed_post_url = urlparse(comment["author"])
            commenter_host = '{}://{}/'.format(parsed_post_url.scheme, parsed_post_url.netloc)
            if (commenter_host == settings.BACKEND_URL):
                # fetch the author profiel and make sure he exisrts
                author_uuid = get_author_profile_uuid(comment["author"])

                author_profile = AuthorProfile.objects.filter(id=author_uuid)
                if (author_profile.exists()):
                    comment["author"] = AuthorProfileSerializer(author_profile[0]).data
                    comments.append(comment)
            else:
                # do foreigner stuff
                if (ServerUser.objects.filter(host=commenter_host).exists()):
                    try:
                        foreign_author_id = get_author_profile_uuid(comment["author"])
                        server_obj = ServerUser.objects.get(host=commenter_host)
                        url = "{}{}author/{}".format(server_obj.host, server_obj.prefix, foreign_author_id)
                        headers = {'Content-type': 'application/json'}
                        response = requests.get(url,
                                                auth=(server_obj.send_username, server_obj.send_password),
                                                headers=headers
                                                )
                        if (response.status_code == 200):
                            foreign_author = json.loads(response.content)
                            comment["author"] = foreign_author
                            comments.append(comment)

                    except:
                        # To do do a legit way of handling people that dont exist
                        pass
    post["comments"] = comments
    return post


def paginate_posts(request, posts):
    DEFAULT_PAGE = 1
    DEFAULT_PAGE_SIZE = 20

    if len(posts) <= 0:
        return posts

    try:
        page_num = request.GET.get('page', DEFAULT_PAGE)
        page_size = request.GET.get('size', DEFAULT_PAGE_SIZE)

        if page_num <= 0:
            page_num = DEFAULT_PAGE
        if page_size <= 0:
            page_size = DEFAULT_PAGE_SIZE
    except:
        page_num = DEFAULT_PAGE
        page_size = DEFAULT_PAGE_SIZE

    page_size = min(page_size, DEFAULT_PAGE_SIZE)
    paginator = Paginator(posts, page_size)
    paged_result = paginator.get_page(page_num).object_list
    return paged_result
