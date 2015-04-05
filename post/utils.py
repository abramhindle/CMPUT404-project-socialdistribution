from dateutil import parser
from author.models import FriendRequest, Author
from category.models import PostCategory
from comment.models import Comment
from post.models import Post
import node.APICalls as remote_helper
import author.utils as author_utils

import markdown
from socialdistribution.settings import LOCAL_HOST


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


def getVisibleToAuthor(viewer=None, author=None, time_line=False, localOnly=False):
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
                if (viewer == post.author or FriendRequest.is_friend(viewer, author) or
                        FriendRequest.is_following(viewer, author)):
                    resultList.append(get_post_json(post))
            else:
                resultList.append(get_post_json(post))

    if localOnly is False:
        if not time_line:
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

def updatePost(postJson):
    post = Post.objects.filter(guid=postJson['guid'])
    if len(post) > 0:
        post = post.first()
        if 'title' in postJson:
            post.title = postJson['title']

        if 'description' in postJson:
            post.description = postJson['description']

        if 'content-type' in postJson:
            post.content_type = postJson['content-type']

        if 'content' in postJson:
            post.content = postJson['content']

        if 'visibility' in postJson:
            post.visibility = postJson['visibility']

        post.save()
    else:
        if 'author' in postJson:
            authorJson = postJson['author']
            if authorJson['host'] == LOCAL_HOST:
                author = Author.objects.filter(uuid=authorJson['id'])
                if len(author) > 0:
                    author = author.first()
                else:
                    raise Exception("invalid author")
            else:
                raise Exception("invalid author")
        else:
            raise Exception("invalid author")

        post = Post.objects.create(title=postJson['title'],
                                   description=postJson['description'],
                                   content_type=postJson['content-type'],
                                   content=postJson['content'],
                                   guid=postJson['guid'],
                                   visibility=postJson['visibility'],
                                   author=author,
                                   publication_date=parser.parse(postJson['pubDate']))
    if 'comments' in postJson:

        # easiest way to keep comments updated is by deleting exsting comments and adding the new ones
        Comment.removeCommentsForPost(post)

        comments = postJson['comments']
        for comment in comments:
            authorJson = comment['author']
            comment_id = comment['guid']

            commentFilter = Comment.objects.filter(guid=comment_id)
            if len(commentFilter) == 0:
                # no comment exists with the id, add it
                author = Author.objects.filter(uuid=authorJson['id'])

                if len(author) > 0:
                    author = author.first()
                else:
                    author = author_utils.createRemoteUser(displayName=authorJson['displayname'],
                                                         host=authorJson['host'],
                                                         uuid=authorJson['id'])
                comment_text = comment['comment']
                Comment.objects.create(guid=comment_id,
                                       comment=comment_text,
                                       pubDate=parser.parse(comment['pubDate']),
                                       author=author,
                                       post=post)

    if 'categories' in postJson:

        #remove all previous categories and add the new ones
        PostCategory.removeAllCategoryForPost(post)

        categories = postJson['categories']
        for category in categories:
            PostCategory.addCategoryToPost(post, category)

    return get_post_json(post)

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