from comment.models import Comment


# Returns the json object of the post with everything related to the post
def getPostJson(post):

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

    return post_json