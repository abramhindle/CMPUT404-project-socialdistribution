from urllib.parse import urlparse

from ..models import AuthorProfile, Follow, ServerUser
from ..serializers import AuthorProfileSerializer
import urllib
from django.conf import settings
import requests


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

                is_friend_filter = Follow.objects.filter(authorA=post["author"]["id"],
                                                         authorB=requesting_author_id,
                                                         status="FRIENDS")
                # they are direct friends
                if (is_friend_filter.exists()):
                    return True
                else:
                    for friend in friends_list:
                        is_friend_filter = Follow.objects.filter(authorA=friend,
                                                                 authorB=requesting_author_id,
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
