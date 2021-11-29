import uuid
import requests
import time
import json
import threading
import traceback
from concurrent.futures import ThreadPoolExecutor

from .serializers import PostSerializer
from rest_framework.authtoken.models import Token

from .models import Author, Post, Comment, Node, Like, FriendRequest

from .converter import *
from .utils import *
from social_dist.settings import DJANGO_DEFAULT_HOST



def update_db(update_authors: bool, update_posts: bool, time_profile = True):
    """
    This will update the database with remote authors and posts

    args:
        update_authors - If True will get all the authors from the remote node
        update_posts - If True will get all the posts from the remote node

    return
    """
    print("here")
    start_time = time.time()
    foreign_author_id_list = []
    for node in Node.objects.all():
        if not node.connect:
            continue
        # This will add or remove authors on the local db based on the state of the remote node
        foreign_author_ids = update_remote_authors(node.host, node.requesting_auth_info)
        foreign_likes_ids = update_remote_likes(node.host, node.requesting_auth_info, foreign_author_ids)
        # This will add or remove posts on the local db based on the state of the remote node
        foreign_posts_ids = update_remote_posts(node.host, node.requesting_auth_info, foreign_author_ids)
        foreign_comments_ids = update_remote_comments(node.host, node.requesting_auth_info, foreign_posts_ids)


    if time_profile:
        print(f'update_db time taken {time.time() - start_time} s')

def async_update_db(update_authors: bool, update_posts: bool, time_profile=True):
    threading.Thread(target=update_db, name="update_db", args=(update_authors, update_posts, time_profile)).start()


def async_get(url, auth=None, headers=None, params=None, object_instance=None):
    """
    This is a callback function that will async get a json object from the url provided
    """
    res = requests.get(
        url,
        headers=headers,
        auth=auth,
        params=params,
    )
    if res.status_code not in range(200, 300):
        print(f"async_get error: {url} {res.status_code}\nheaders={headers}\nauth={auth}\nparams={params}")
        return {}
    res_dict = res.json()
    res_dict['object_instance'] = object_instance
    return res_dict

def async_post(url, auth=None, headers=None, params=None, data=None):
    """
    This is a callback function that will async post a json object to the url provided
    """
    res = requests.post(
        url,
        headers=headers,
        auth=auth,
        params=params,
        json=data,
    )
    if res.status_code not in range(200, 300):
        print(f"async_post error: {url} {res.status_code}\nheaders={headers}\nauth={auth}\nparams={params}\ndata={data}")
        return {}
    res_dict = res.json()
    return res_dict

def send_post_to_foreign_authors(post: Post):
    """
    Helper function to send to all foreign authors' inboxes
    """
    try:
        remote_authors = Author.objects.filter(user__isnull=True)
        for author in remote_authors:
            author_inbox_url = author.url + '/inbox/'
            post_dict = PostSerializer(post).data
            res = requests.post(
                author_inbox_url,
                json=post_dict, 
            )

            if res.status_code not in range(200, 300):
                print(f"Something went wrong with the sending\n\n{res.status_code} {res.text}")
    except Exception as e:
        print("send_post_to_foreign_authors Exception: {}\n\n{}".format(type(e), str(e)))

def send_to_friends(author: Author, payload: dict):
    """
    This will send payload to all the authors' friend inbox

    args:
        author: The author object to send from
        payload: The json object to send
    """
    try:
        internal_post_dict = sanitize_post_dict(payload)

        followers = list(author.followers.all())
        friend_url_list = []
        auth_info_list = []
        header_list = []
        param_list = []
        data_list = []
        # Get the auth for the author for local friends
        author_token = Token.objects.get(user=author.user).key
        # Setup the request for all friends
        for follower in followers:
            friend = get_friend(author, follower.id)
            # If friend
            if friend == None:
                continue
            # Setup the inbox url to the friend
            friend_url = follower.url + '/inbox/'
            # If the friend is local then we directly add the post to their inbox model
            if DJANGO_DEFAULT_HOST.split('//')[1].split('/api/')[0] in friend_url:
                friend_inbox = Inbox.objects.get(id=follower)
                post = Post.objects.get(id=internal_post_dict['id'])
                friend_inbox.posts.add(post)
                continue
            # Strip off the schema
            node = Node.objects.get(host__icontains=str(friend.host).split('//')[1])
            user, passwd = str(node.requesting_auth_info).split(':')
            auth_info = (user, passwd)
            post_header = None
            friend_url_list.append(friend_url)
            auth_info_list.append(auth_info)
            header_list.append(post_header)
            param_list.append(None)
            data_list.append(payload)

        with ThreadPoolExecutor(max_workers=1) as pool:
            res_friend_inbox_obj_list = list(pool.map(async_post, friend_url_list, auth_info_list, header_list, param_list, data_list))
            
    except Exception as e:
        print("send_to_friends Exception: {}\n\n{}\n\n{}".format(type(e), str(e), traceback.format_exc()))



# Update Posts
def update_remote_posts(host: str, auth: str, foreign_author_ids: list, time_profile = True):
    """
    Update remote posts based on the list of foreign author ids
    
    Return:
        Will return a list of ids from valid (sanitized posts) from the remote host
    """
    try:
        start_time = time.time()
        remote_authors_host = Author.objects.filter(id__in=foreign_author_ids).values_list('url', flat=True)
        post_dict_list = []

        with ThreadPoolExecutor(max_workers=1) as pool:
            urls = [author_url + '/posts/' for author_url in remote_authors_host]
            user, passwd = auth.split(':')
            auths = [(user, passwd)]*len(urls)
            headers = [{'Accept': 'application/json'}]*len(urls)
            params = [{'page':1, 'size': 1000}]*len(urls)
            res_post_obj_list = list(pool.map(async_get, urls, auths, headers, params))

            for res_post_obj in res_post_obj_list:
                for raw_post in res_post_obj['items']:
                    post = sanitize_post_dict(raw_post, host)
                    if post == None:
                        continue
                    post_dict_list.append(post)
            # Add, update or delete posts based on the foreign state
            CRUD_remote_post(host, auth, post_dict_list)

    except Exception as e:
        print("update_remote_posts exception : {}\n\n{}".format(type(e), str(e)))
        return []
    
    if time_profile:
        print(f'update_remote_posts time taken {time.time() - start_time} s')
    
    return [post['id'] for post in post_dict_list]

def CRUD_remote_post(host: str, auth: str, post_dict_list: list):
    """
    This will create, update or delete posts on the local database based on the remote response
    """
    try:
        for post_dict in post_dict_list:
            post, created = Post.objects.update_or_create(id=post_dict['id'], defaults=post_dict)

        ids = [post['id'] for post in post_dict_list]
        # remove the schema from the host 
        stripped_url = host.split('//')[1]
        Post.objects.filter(url__icontains=stripped_url).exclude(id__in=ids).delete()

    except Exception as e:
        print("CRUD_remote_post exception : {}\n\n{}".format(type(e), str(e)))

# Update comments
def update_remote_comments(host: str, auth: str, foreign_post_ids: list, time_profile = True):
    """
    This will update remote comments based on the list of foreign posts.

    Return:
        Will return a list of ids from valid (sanitized comments) from the remote host
    """
    try:
        start_time = time.time()
        remote_comment_url_post_id = Post.objects.filter(id__in=foreign_post_ids).values_list('comment_url', 'id')
        comment_dict_list = []

        with ThreadPoolExecutor(max_workers=1) as pool:
            urls = [comment_url_post_id[0] for comment_url_post_id in remote_comment_url_post_id]
            post_objs = [Post.objects.get(id=comment_url_post_id[1]) for comment_url_post_id in remote_comment_url_post_id]
            user, passwd = auth.split(':')
            auths = [(user, passwd)]*len(urls)
            headers = [{'Accept': 'application/json'}]*len(urls)
            params = [{'page':1, 'size': 1000}]*len(urls)
            res_comment_obj_list = list(pool.map(async_get, urls, auths, headers, params, post_objs))

            for res_comment_obj in res_comment_obj_list:
                post_obj = res_comment_obj['object_instance']
                for raw_comment in res_comment_obj['comments']:
                    comment = sanitize_comment_dict(raw_comment, post_obj, host)
                    # If comment is None or the key 'id' is not in comment then we ignore it.
                    if comment == None or 'id' not in comment:
                        continue
                    comment_dict_list.append(comment)
            CRUD_remote_comments(host, auth, comment_dict_list)
    except Exception as e:
        print("update_remote_comments exception : {}\n\n{}".format(type(e), str(e)))
        return []

    if time_profile:
        print(f'update_remote_comments time taken {time.time() - start_time} s')

    return [comment['id'] for comment in comment_dict_list]

def CRUD_remote_comments(host: str, auth: str, comment_dict_list: list):
    """
    This will create, update or delete comments from a post
    """
    try:
        for comment_dict in comment_dict_list:
            comment, created = Comment.objects.update_or_create(id=comment_dict['id'], defaults=comment_dict)

        ids = [comment['id'] for comment in comment_dict_list]
        # Remove the schema from the url
        stripped_host = host.split('//')[1]
        Comment.objects.filter(url__icontains=stripped_host).exclude(id__in=ids).delete()

    except Exception as e:
        print("CRUD_remote_comments Exception : {}\n\n{}".format(type(e), str(e)))

# Update likes
def update_remote_likes(host: str, auth: str, foreign_author_ids: list, time_profile = True):
    try:
        start_time = time.time()
        remote_authors_host = Author.objects.filter(id__in=foreign_author_ids).values_list('url', flat=True)
        likes_dict_list = []

        with ThreadPoolExecutor(max_workers=1) as pool:
            urls = [author_url + '/liked' for author_url in remote_authors_host]
            user, passwd = auth.split(':')
            auths = [(user, passwd)]*len(urls)
            headers = [{'Accept': 'application/json'}]*len(urls)
            params = [{'page':1, 'size': 1000}]*len(urls)

            res_likes_obj_list = list(pool.map(async_get, urls, auths, headers, params))

            for res_likes_obj in res_likes_obj_list:
                for raw_likes in res_likes_obj['items']:
                    likes = sanitize_like_dict(raw_likes)
                    if likes == None:
                        continue
                    likes_dict_list.append(likes)
        
            CRUD_remote_likes(likes_dict_list)
    except Exception as e:
        print("update_remote_likes exception : {}\n\n{}".format(type(e), str(e)))
        return []

    if time_profile:
        print(f'update_remote_likes time taken {time.time() - start_time} s')

    # Return a list of like object id's which is a pair of author id and the object being liked 
    # from the remote server
    return [(likes['author'].id, likes['object']) for likes in likes_dict_list]

def CRUD_remote_likes(likes_dict_list: list):
    try:
        for like_dict in likes_dict_list:
            like, created = Like.objects.get_or_create(
                object=like_dict['object'], 
                author=like_dict['author'],
                defaults=like_dict)
        
    except Exception as e:
        print("CRUD_remote_likes exception : {}\n\n{}".format(type(e), str(e)))

# Update Author
def update_remote_authors(host: str, auth: str, time_profile = True):
    """
    This will make an author API request to the host using auth to get the list of current authors on the remote note and updating our database accordingly

    args:
        host - The host url of the remote server
        auth - The authentication information to send to the server

    returns:
        foreign_ids - The list of foreign ids from the host
    """
    start_time = time.time()
    author_dict_list = []
    try:
        url = host + 'authors/'
        query = {'page': 1, 'size': 1000}
        user, passwd = auth.split(':')
        res = requests.get(
            url,
            headers = {'Accept': 'application/json'},
            auth=(user, passwd),
            params=query
        )
        if res.status_code not in range(200, 300):
            raise Exception(str(res.text))
        raw_author_dict_list = res.json()
        for raw_author_dict in raw_author_dict_list['items']:
            author_dict = sanitize_author_dict(raw_author_dict)
            if author_dict == None:
                continue
            author_dict_list.append(author_dict)

        CRUD_remote_authors(host, author_dict_list)
    except Exception as e:
        print("update_remote_authors exception : {}\n\n{}".format(type(e), str(e)))

    if time_profile:
        print(f'update_remote_authors {time.time() - start_time} s')

    return [author_dict['id'] for author_dict in author_dict_list]

def CRUD_remote_authors(host: str, author_dict_list: list):
    """
    This will create, update or delete authors on the local database based on the remote response

    args:
        host - The host of the remote server/node
        author_dict_list - The list of author in dict form to check the db
    """
    try:
        for author_dict in author_dict_list:
            Author.objects.update_or_create(id=author_dict['id'], defaults=author_dict)

        ids = [author_dict['id'] for author_dict in author_dict_list]
        Author.objects.filter(host=host).exclude(id__in=ids).delete()

    except Exception as e:
        print("CRUD_remote_authors exception : {}\n\n{}".format(type(e), str(e)))