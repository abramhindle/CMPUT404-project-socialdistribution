from comment.models import Comment
from post.models import Post
from author.models import FriendRequest, Author


AUTHOR = "author"
POST = "post"


def _get_posts(request, id, type):
    user = request.user if request.user.is_authenticated() else None
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
        post_json = post.getJsonObj()

        comment_list = []
        comments = Comment.getCommentsForPost(post)
        for comment in comments:
            comment_list.append(comment.getJsonObj())

        # category_list = []
        # categories = Category.getCategoryForPost(post)
        # for category in categories:
        # category_list.append(category.getStr())

        post_json['comments'] = comment_list
        # post_json['categories'] = category_list
        post_list.append(post_json)
    return post_list