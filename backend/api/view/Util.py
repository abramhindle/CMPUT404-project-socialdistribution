from ..models import AuthorProfile, Follow

def can_read(request, post):
    try:
        current_author_profile = AuthorProfile.objects.get(user=request.user)
        current_author_id = "{}author/{}".format(current_author_profile.host, str(current_author_profile.id))
        if(current_author_id == post["author"]["id"] or post["unlisted"] == True or post["visibility"] == "PUBLIC"):
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
                            print("yay")
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