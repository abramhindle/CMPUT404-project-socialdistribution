import os
import uuid
host_url = os.getenv('HOST', 'http://localhost:8000/service')

def build_url(*args, host:str=host_url):
    """
    Build a URL from the given host and path components.
    """
    return host + '/' + '/'.join(args)

def build_author_url(author_id:str, host:str=host_url):
    """
    Build an author URL from the given host and author ID.
    """
    return build_url('authors', author_id, host=host)

def build_post_url(author_id:str, post_id:str, host:str=host_url):
    """
    Build a post URL from the given host and post ID.
    """
    return build_url('authors', author_id, 'posts', post_id, host=host)

def create_author_url(host:str=host_url):
    """
    Build an author URL from the given host and author ID.
    """
    author_id = str(uuid.uuid4())
    return build_url('authors', author_id, host=host)

def create_post_url(author_url:str):
    """
    Build a post URL from the given author URL and post ID.
    """
    post_id = str(uuid.uuid4())
    return build_url('posts', post_id, host=author_url)

def create_comment_url(post_url:str):
    """
    Build a comment URL from the given post URL and comment ID.
    """
    comment_id = str(uuid.uuid4())
    return build_url('comments', comment_id, host=post_url)

def build_comment_url(author_id:str, post_id:str, comment_id:str, host:str=host_url):
    """
    Build a comment URL from the given host and comment ID.
    """
    return build_url('authors', author_id, 'posts', post_id, 'comments', comment_id, host=host)