from post.models import Post
import post.utils as post_utils
from author.models import FriendRequest, Author


AUTHOR = "author"
POST = "post"


def _get_posts(request, id, type):
    if type == AUTHOR:
        user = request.user
        if id is not None:
            author = Author.objects.filter(uuid=id)
            if len(author) > 0:
                author = author[0]
            else:
                return {'posts': []}
            posts = Post.getVisibleToAuthor(user, author)
        else:
            posts = Post.getVisibleToAuthor(user)

    else:
        if id is not None:
            post = Post.getPostById(id)
            if post is not None:
                return post.getJsonObj()
            else:
                return {}
        else:
            posts = Post.getVisibleToAuthor()

    post_list = _get_post_list(posts)
    return {'posts': post_list}


def _get_post_list(posts):
    post_list = []
    for post in posts:
        post_list.append(post_utils.get_post_json(post))
    return post_list


def getRemoteUserHost(user_id):
    try:
        authors = Author.objects.filter(uuid__endswith=user_id)
        if len(authors) == 1:
            return authors
        else:
            return None  # hmmm why was there more than one
    except:
        return None