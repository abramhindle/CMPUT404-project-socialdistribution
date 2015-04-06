import json
from author.models import FriendRequest
from category.models import PostCategory
from comment.models import Comment
from post.models import Post
import node.APICalls as remote_helper

import markdown


def deletePost(postId):
    Post.objects.filter(guid=postId).delete()


def getVisibilityTypes():
    visFriendlyString = {
        'private': 'Private',
        'author': 'Another Author',
        'friends': 'Friends',
        'foaf': 'Friends of Friends',
        'serverOnly': 'Server Only',
    }
    return visFriendlyString

# Gets a list of posts visible to the viewer by the author, by default,
# all public posts are returned


def getVisibleToAuthor(viewer=None, author=None, time_line=False):
    # TODO add another paramenter for timeline only posts
    resultList = []
    if author is None:
        postList = Post.objects.all()
    else:
        postList = Post.objects.filter(author=author)

    for post in postList:
        if post.isViewable(viewer, post.author):
            # if we are should timeline only, then we need to check whether or not the
            # two are friends
            if post.content_type == Post.MARK_DOWN:
                post.content = markdown.markdown(
                    post.content, safe_mode='escape')

            if time_line:
                if (viewer == post.author or FriendRequest.is_friend(viewer, post.author) or
                        FriendRequest.is_following_or_made_request(viewer, post.author)):
                    resultList.append(get_post_json(post))
            else:
                resultList.append(get_post_json(post))

    if author is None and not time_line:
        remote_posts = remote_helper.api_getPublicPost()
    else:
        authorID = author.get_uuid() if author is not None else None
        remote_posts = remote_helper.api_getPostByAuthorID(viewer, authorID)

    resultList.extend(remote_posts)

    return resultList


def getByAuthor(author):
    return Post.objects.filter(author=author)


def getPostById(id, viewer=None):
    try:
        post = Post.objects.get(guid=id)
    except:
        post = None

    return post if post != None and post.isViewable(viewer, post.author) else None

# Returns the json object of the post with everything related to the post


def get_post_json(post):

    post_json = post.getJsonObj()

    comment_list = []
    comments = Comment.getCommentsForPost(post)
    for comment in comments:
        comment_list.append(comment.getJsonObj())

    category_list = []
    categories = PostCategory.getCategoryForPost(post)
    if categories is not None:
        for category in categories:
            category_list.append(category.name)

    post_json['comments'] = comment_list
    post_json['categories'] = category_list

    return post_json
