# This will convert the dict from the public space to the dict required for our models

def sanitize_author_dict(author:dict):
    """
    This will sanitize or convert the author dict to a dict that matches our model

    args:
        author - The dict of the author to convert/sanitize
    
    return - A new dict of the converted/sanitized object
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

def sanitize_post_dict(post: dict):
    """
    This will sanitize or convert the post dict to a dict that matches our model

    args:
        post - The dict of the post to convert/sanitize
    
    return: A new dict of the converted/sanitized object
    """
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
    if 'origin' in post:
        convert_post['origin'] = post['origin']
    if 'description' in post:
        convert_post['description'] = post['description']
    if 'content' in post:
        convert_post['content'] = post['content']
           
    return convert_post