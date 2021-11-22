# This will convert the dict from the public space to the dict required for our models

def sanitize_author_dict(author: dict):
    """
    This will sanitize or convert the author dict to a dict that matches our model

    args:
        author - The dict of the author to convert/sanitize

    returns: 
        - A new dict of the converted/sanitized object.
        - If there is an error a None is returned
    """
    try:
        convert_author = {
            'id': author['url'].split('/')[-1],
            'url': author['url'],
            'host': author['host'],
        }
        if 'profileImage' in author:
            convert_author['profile_image'] = author['profileImage']
        if 'displayName' in author:
            convert_author['display_name'] = author['displayName'],
        if 'github' in author:
            convert_author['github_url'] = author['github']
        # TODO: maybe copy over followers as well
    except:
        return None
    return convert_author


def sanitize_post_dict(post: dict, node: str = None):
    """
    This will sanitize or convert the post dict to a dict that matches our model

    args:
        post - The dict of the post to convert/sanitize

    returns: 
        - A new dict of the converted/sanitized object
        - If there is an error a None is returned
    """
    try:
        # These are required fields
        convert_post = {
            'id': post['id'].split('/')[-1],
            'url': post['id'],
            'content_type': post['contentType'],
            # assuming that the author dict is in the public form
            'author': sanitize_author_dict(post['author']),
            'published': post['published'],
            'visibility': post['visibility'],
            'comment_url': post['comments'],
            'unlisted': post['unlisted'],
        }
        # These are optional fields
        if 'source' in post:
            convert_post['source'] = post['source']
        if 'categories' in post:
            convert_post['categories'] = post['categories']
        if 'origin' in post:
            convert_post['origin'] = post['origin']
        if 'description' in post:
            convert_post['description'] = post['description']
        if 'content' in post:
            convert_post['content'] = post['content']
    except:
        return None
    return convert_post


def sanitize_comment_dict(comment: dict, node: str = None):
    try:
        convert_comment = {
            'author': sanitize_author_dict(comment['author']),
            'comment': comment['comment'],
            'content_type': comment['contentType'],
            'published': comment['published'],
            'id': comment['id'].split('/')[-1]
        }
    except:
        return None
    return convert_comment


def sanitize_like_dict(like: dict, node: str = None):
    try:
        convert_like = {
            'summary': like['summary'],
            'object': like['object'],
            'author': sanitize_author_dict(like['author']),
        }
    except:
        return None
    return convert_like
