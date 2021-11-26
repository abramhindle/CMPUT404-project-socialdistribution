# This will convert the dict from the public space to the dict required for our models

from .models import Author, Post
import uuid

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
        if author['url'][-1] == '/':
            author['url'] = author['url'][0:-1]
        
        converted_author = {
            'id': author['url'].split('/')[-1],
            'url': author['url'],
            'host': author['host'],
        }
        if 'profileImage' in author:
            converted_author['profile_image'] = author['profileImage']
        if 'displayName' in author:
            converted_author['display_name'] = author['displayName']
        if 'github' in author:
            converted_author['github_url'] = author['github']
    except Exception as e:
        print("sanitize author exception : {}\n\n{}".format(type(e), str(e)))
        return None
    return converted_author

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
        # assuming that the author dict is in the public form
        author_dict = sanitize_author_dict(post['author'])
        author, created = Author.objects.get_or_create(id=author_dict['id'], defaults=author_dict)
        # These are required fields
        if post['id'][-1] == '/':
            post['id'] = post['id'][0:-1]
        converted_post = {
            'id': post['id'].split('/')[-1],
            'url': post['id'],
            'content_type': post['contentType'],
            # This should be an Author Object
            'author': author,
            'published': post['published'],
            'visibility': post['visibility'],
            'comment_url': post['comments'],
            'unlisted': post['unlisted'],
        }
        # If the node is none then we assume that the source of the post is the same as the author's host
        if node == None:
            converted_post['source'] = author_dict['host']
        else:
            converted_post['source'] = node
        # These are optional fields
        if 'categories' in post:
            converted_post['categories'] = post['categories']
        if 'origin' in post:
            converted_post['origin'] = post['origin'].split('posts/')[0]
        else:
            converted_post['origin'] = node
        if 'description' in post:
            converted_post['description'] = post['description']
        if 'content' in post:
            converted_post['content'] = post['content']
        if 'title' in post:
            converted_post['title'] = post['title']

    except Exception as e:
        print("sanitize post exception : {}\n\n{}".format(type(e), str(e)))
        return None
    return converted_post


def sanitize_comment_dict(comment: dict, post_obj: Post, node: str = None):
    try:
        author_dict = sanitize_author_dict(comment['author'])
        author, created = Author.objects.get_or_create(id=author_dict['id'], defaults=author_dict)
        converted_comment = {
            'author': author,
            'comment': comment['comment'],
            'post': post_obj,
        }
        # If the content is there then it should assign it
        if 'contentType' in comment:
            converted_comment['content_type'] = comment['contentType']
        # If published is not found then it's assume that we are generating one from scratch on creation
        if 'published' in comment:
            converted_comment['published'] = comment['published']
        # If the if the id is there then we assume that we are importing a comment
        if 'id' in comment:
            if comment['id'][-1] == '/':
                comment['id'] = comment['id'][0:-1]
            converted_comment['id'] = comment['id'].split('/')[-1]
        # If the id is missing then it's assume that we are generating one from scratch on creation
    
    except Exception as e:
        print("sanitize comment exception : {}\n\n{}".format(type(e), str(e)))
        return None
    return converted_comment


def sanitize_like_dict(like: dict, node: str = None):
    try:
        author_dict = sanitize_author_dict(like['author'])
        author, created = Author.objects.get_or_create(id=author_dict['id'], defaults=author_dict)
        converted_like = {
            'summary': like['summary'],
            'object': like['object'],
            'author': author,
        }
    except Exception as e:
        print("sanitize like exception : {}\n\n{}".format(type(e), str(e)))
        return None
    return converted_like

def sanitize_friend_request_dict(friend_request: dict, node: str = None):
    try:
        actor_dict = sanitize_author_dict(friend_request['actor'])
        object_dict = sanitize_author_dict(friend_request['object'])
        # Get or create the actor and get the object
        actor, created = Author.objects.get_or_create(id=actor_dict['id'], defaults=actor_dict)
        object = Author.objects.get(id=object_dict['id'])
        converted_friend_request = {
            'summary': friend_request['summary'],
            'actor': actor,
            'object': object
        }
    except Exception as e:
        print("sanitize friend request exception : {}\n\n{}".format(type(e), str(e)))
        return None
    return converted_friend_request
