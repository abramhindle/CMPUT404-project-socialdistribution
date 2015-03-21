from post.models import Post
import post.utils as post_utils
from author.models import FriendRequest, Author


AUTHOR = "author"
POST = "post"


def _get_posts(request, id, type):
    user = request.user
    if type == AUTHOR:
        if id is not None:
            posts = Post.getVisibleToAuthor(user, Author.objects.get(uuid=id))
        else:
            posts = Post.getVisibleToAuthor(user)

    else:
        if id is not None:
            posts = [Post.getPostById(id)]
        else:
            posts = Post.getVisibleToAuthor()

    post_list = _get_post_list(posts)
    return {'posts': post_list}


def _get_post_list(posts):
    post_list = []
    for post in posts:
        post_list.append(post_utils.getPostJson(post))
    return post_list