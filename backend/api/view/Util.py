from ..models import AuthorProfile, Follow
from ..serializers import AuthorProfileSerializer
import urllib


def get_author_id(author_profile, escaped):
    # print(AuthorProfileSerializer(author_profile).data)
    formated_id = AuthorProfileSerializer(author_profile).data["id"]
    if(escaped):
        formated_id = urllib.parse.quote(formated_id, safe='~()*!.\'')
    return formated_id


def can_read(request, post):
    try:
        # todo: Check if author does not belong to our server for cross server
        current_author_profile = AuthorProfile.objects.get(user=request.user)
        current_author_id = get_author_id(current_author_profile, False)

        if(current_author_id == post["author"]["id"] or post["visibility"] == "PUBLIC"):
            return True

        elif post["unlisted"]:
            return False

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
                # todo change this server_host variable
                server_host = "http://127.0.0.1:5454/"
                if(current_author_profile.host == server_host):
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

def in_server_nodes_list(request):
    request_server = request.build_absolute_uri('/')
    result = Nodes.objects.filter(server=request_server)
    if(result.exists()):
        return True
    return False
