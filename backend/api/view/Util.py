from urllib.parse import urlparse
from rest_framework.response import Response
from ..models import AuthorProfile, Follow, Post, Comment, ServerUser
from ..serializers import AuthorProfileSerializer, CommentSerializer, PostSerializer
import urllib
from django.conf import settings
import requests
import json

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

def validate_uuid(author_id):
    try:
        uuid.UUID(author_id)
        return True
    except:
        return False


#posts is a list of post
#author full id includes the id
# is own posts
def build_post(post):
    comments = []
    if("comments" in post):
        # do stuff
        for comment in post["comments"]:
            # full_author_id = comment["author"] # http://localhost:8000/author/adfhadifnads
            parsed_post_url = urlparse(comment["author"])
            commenter_host = '{}://{}/'.format(parsed_post_url.scheme, parsed_post_url.netloc)
            if(commenter_host == settings.BACKEND_URL):
                # fetch the author profiel and make sure he exisrts
                author_uuid = get_author_profile_uuid(comment["author"])

                author_profile = AuthorProfile.objects.filter(id=author_uuid)
                if(author_profile.exists()):
                    comment["author"] = AuthorProfileSerializer(author_profile[0]).data
                    comments.append(comment)
            else:
                # do foreigner stuff    
                if(ServerUser.objects.filter(host=commenter_host).exists()):
                    try:
                        foreign_author_id = get_author_profile_uuid(comment["author"])
                        server_obj = ServerUser.objects.get(host=commenter_host)
                        url = "{}{}author/{}".format(server_obj.host, server_obj.prefix, foreign_author_id)
                        headers = {'Content-type': 'application/json'}
                        response = requests.get(url,
                                            auth=(server_obj.send_username, server_obj.send_password),
                                            headers=headers
                                            )
                        if(response.status_code == 200):
                            foreign_author = json.loads(response.content)
                            comment["author"] = foreign_author
                            comments.append(comment)
                        
                    except:
                        #To do do a legit way of handling people that dont exist
                        pass
    post["comments"] = comments
    return post
