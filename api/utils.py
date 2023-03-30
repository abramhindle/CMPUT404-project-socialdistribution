import os
import uuid
HOST_URL = os.getenv('HOST', 'http://localhost:8000')
PREFIX = 'service'
KNOWN_TEAMS = {
    'https://sd7-api.herokuapp.com': 'TEAM_7',
    'https://cmput404-project-data.herokuapp.com': 'TEAM_12',
    HOST_URL: 'TEAM_16',
    'https://social-distribution-w23-t17.herokuapp.com': 'TEAM_17',
}

def which_node(url:str, return_host=False):
    """
    Return the node name of the given URL.
    
    Returns 'TEAM_X' where 'X' is the team number. If return_host is True, then
    the host of the url is returned instead of the team name.
    Return 'TEAM_UNKNOWN' if we do not recognize the url. 
    """
    # This is so that we can still determine which team the url belongs to even
    # if they are not useing https.
    if url.startswith('http://') and url != 'http://localhost:8000':
        url = url.replace('http://', 'https://', 1)
           
    # Get the TEAM_X name of the given url.
    for host in KNOWN_TEAMS.keys():
        if url.startswith(host):
            return KNOWN_TEAMS[host] if not return_host else host
    return 'TEAM_UNKNOWN'
    

def build_url(*args, host:str=HOST_URL):
    """Build a URL from the given host and path components."""
    return host + '/' + '/'.join(args)


def build_author_url(author_id:str, host:str=HOST_URL, prefix:str=PREFIX):
    """Build an author URL from the given host and author ID."""
    return build_url(prefix, 'authors', author_id, host=host)


def build_post_url(author_id:str, post_id:str, host:str=HOST_URL, prefix:str=PREFIX):
    """Build a post URL from the given host and post ID."""
    return build_url(prefix, 'authors', author_id, 'posts', post_id, host=host)


def create_author_url(host:str=HOST_URL, prefix:str=PREFIX):
    """
    Build an author URL with a generated author_id.
    
    returns: str
        - the author URL of the form <host>/<prefix>/authors/<author_id>
    """
    author_id = str(uuid.uuid4())
    return build_url(prefix, 'authors', author_id, host=host)


def create_post_url(author_url:str):
    """
    Build a post URL with a generated post_id.
    
    Parameters:
    - author_url: str
        - a URL of the form <host>/<prefix>/authors/<author_id>
    
    returns: str
        - the post URL of the form <author_url>/posts/<post_id>
    """
    post_id = str(uuid.uuid4())
    return build_url('posts', post_id, host=author_url)


def create_comment_url(post_url:str):
    """
    Build a comment URL with a generated comment_id.
    
    Parameters:
    - post_url: str
        - a URL of the form <host>/<prefix>/authors/<author_id>/posts/<post_id>
    
    returns: str
        - the post URL of the form <post_url>/comments/<comment_id>
    """
    comment_id = str(uuid.uuid4())
    return build_url('comments', comment_id, host=post_url)


def build_comment_url(author_id:str, post_id:str,
                      comment_id:str, host:str=HOST_URL, prefix:str=PREFIX):
    """
    Build a comment URL of the form
    <host>/<prefix>/authors/<author_id>/posts/<post_id>/comments/<comment_id>
    """
    return build_url(prefix, 'authors', author_id,
                     'posts', post_id, 'comments', comment_id, host=host)