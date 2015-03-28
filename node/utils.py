from post.models import Post
import post.utils as post_utils
from author.models import FriendRequest, Author


AUTHOR = "author"
POST = "post"


def _get_posts(request, id, type):
    if type == AUTHOR:
        viewer = []
        if(request.user.username != ''):
            viewer = Author.objects.filter(user=request.user)
        if len(viewer) > 0:
            viewer = viewer[0]
        else:
            viewer = None

        if id is not None:
            author = Author.objects.filter(uuid=id)
            if len(author) > 0:
                author = author[0]
            else:
                return {'posts': []}
            posts = post_utils.getVisibleToAuthor(viewer, author)
        else:
            posts = post_utils.getVisibleToAuthor(viewer)

    else:
        if id is not None:
            post = post_utils.getPostById(id)
            if post is not None:
                return post.getJsonObj()
            else:
                return {}
        else:
            posts = post_utils.getVisibleToAuthor()

    return {'posts': posts}


def getRemoteUserHost(user_id):
    try:
        authors = Author.objects.filter(uuid__endswith=user_id)
        if len(authors) == 1:
            return authors
        else:
            return None  # hmmm why was there more than one
    except:
        return None
