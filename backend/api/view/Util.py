from urllib.parse import urlparse

from ..models import AuthorProfile, Follow, Post, Comment
from ..serializers import AuthorProfileSerializer, CommentSerializer, PostSerializer
import urllib
from django.conf import settings


def get_author_id(author_profile, escaped):
    formated_id = AuthorProfileSerializer(author_profile).data["id"]
    if(escaped):
        formated_id = urllib.parse.quote(formated_id, safe='~()*!.\'')
    return formated_id

# the post argument should be a serialized post object
def can_read(current_author_id, post):
    try:
        # todo: Check if author does not belong to our server for cross server

        if(post["unlisted"]):
            return False

        elif(current_author_id == post["author"]["id"] or post["visibility"] == "PUBLIC"):
            return True

        else:
            # check FOAF
            if(post["visibility"] == "FOAF"):

                friends_list = Follow.objects.filter(authorA=post["author"]["id"],
                                                     authorB=current_author_id,
                                                     status="FRIENDS")
                if (friends_list.exists()):
                    return True
                else:
                    friends_list = Follow.objects.filter(authorA=post["author"]["id"],
                                                         status="FRIENDS")
                    foaf_list = friends_list
                    for friend in friends_list:
                        foaf_list = Follow.objects.filter(authorA=friend.authorB,
                                                          authorB=current_author_id,
                                                          status="FRIENDS")
                        if(foaf_list.exists()):

                            return True
                    return False
            # check FRIENDS
            elif(post["visibility"] == "FRIENDS"):
                friends_list = Follow.objects.filter(authorA=post["author"]["id"],
                                                     authorB=current_author_id,
                                                     status="FRIENDS")
                if(friends_list.exists()):
                    return True
                else:
                    return False
            # check PRIVATE
            elif (post["visibility"] == "PRIVATE"):
                if(current_author_id in post["visibleTo"]):
                    return True
                else:
                    return False
            # check SERVERONLY
            elif (post["visibility"] == "SERVERONLY"):
                parsed_url = urlparse(current_author_id)
                author_host = '{}://{}/'.format(parsed_url.scheme, parsed_url.netloc)
                if(author_host == settings.BACKEND_URL):
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
    if("author/" in unquoted_parse):
        author_data = unquoted_parse.split("author/")
        return author_data[1]
    else:
        return None
