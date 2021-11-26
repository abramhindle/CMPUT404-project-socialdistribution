import uuid
import requests

from backend.serializers import PostSerializer

from .models import Author, Post, Comment, Node, Like, FriendRequest
from .converter import *
from social_dist.settings import DJANGO_DEFAULT_HOST

def update_db(update_authors: bool, update_posts: bool):
    """
    This will update the database with remote authors and posts

    args:
        update_authors - If True will get all the authors from the remote node
        update_posts - If True will get all the posts from the remote node

    return
    """
    foreign_author_id_list = []
    for node in Node.objects.all():
        # This will add or remove authors on the local db based on the state of the remote node
        if update_authors:
            foreign_ids = update_remote_authors(node.host, node.requesting_auth_info)
            foreign_author_id_list.extend(foreign_ids)
        # This will add or remove posts on the local db based on the state of the remote node
        if update_posts:
            update_remote_posts(node.host, node.auth_info)

    # This will update the friend list on our local authors
    # if update_authors:
    #     Author.objects.exclude(host=DJANGO_DEFAULT_HOST).exclude(id__in=foreign_author_id_list).delete()

"""
Update Post and Comments
"""


def update_remote_posts(host: str, auth: str):
    try:
        remote_authors_host = Author.objects.filter(user__isnull=True).values_list('url', flat=True)
        post_dict_list = []
        for author_url in remote_authors_host:
            url = author_url + '/posts/'
            res = requests.get(
                url,
                headers={'Authorization': "Basic {}".format(
                    auth), 'Accept': 'application/json'},
                params={'page':'1', 'size': 1000}
            )
            if res.status_code not in range(200, 300):
                continue
            raw_post_list = res.json()
            for raw_post in raw_post_list['items']:
                post = sanitize_post_dict(raw_post, host)
                if post == None:
                    continue
                post_dict_list.append(post)

        CRUD_remote_post(host, auth, post_dict_list)

    except Exception as e:
        print("update_remote_posts exception : {}\n\n{}".format(type(e), str(e)))


def CRUD_remote_post(host: str, auth: str, post_dict_list: list):
    """
    This will create, update or delete posts on the local database based on the remote response
    """
    try:
        for post_dict in post_dict_list:
            post, created = Post.objects.update_or_create(
                id=post_dict['id'], defaults=post_dict)
            CRUD_remote_comments(host, auth, post)

        ids = [post['id'] for post in post_dict_list]
        Post.objects.filter(url__icontains=host).exclude(id__in=ids).delete()
    except Exception as e:
        print("CRUD_remote_post exception : {}\n\n{}".format(type(e), str(e)))

def send_post_to_foreign_authors(post: Post):
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
        print("send_post_to_foreign_authors : {}\n\n{}".format(type(e), str(e)))

def CRUD_remote_comments(host: str, auth: str, post_obj: Post):
    """
    This will create, update or delete comments from a post
    """
    try:
        url = post_obj.comment_url
        query = {'page': 1, 'size': 10000}
        headers = {'Authorization': "Basic {}".format(
            auth), 'Accept': 'application/json'}
        res = requests.get(
            url,
            headers=headers,
            params=query,
        )
        if res.status_code not in (200, 300):
            return None
        raw_comment_dict_list = res.json()['comments']
        ids = []
        for raw_comment_dict in raw_comment_dict_list:
            comment_dict = sanitize_comment_dict(raw_comment_dict, post_obj)
            comment, created = Comment.objects.update_or_create(
                id=comment_dict['id'], defaults=comment_dict)
            ids.append(comment_dict['id'])

        # Comment.objects.filter(url__icontains=url).exclude(id__in=ids).delete()
    except Exception as e:
        print("CRUD_remote_comments Exception : {}\n\n{}".format(type(e), str(e)))


"""
Update Likes
"""


def CRUD_likes(host: str, auth: str, author_dict: dict):
    try:
        url = author_dict['url'] + '/liked'
        headers = {'Authorization': "Basic {}".format(
            auth), 'Accept': 'application/json'}
        res = requests.get(
            url,
            headers=headers,
        )
        if res.status_code not in (200, 300):
            return None
        raw_likes_dict_list = res.json()
        ids = []
        for raw_like_dict in raw_likes_dict_list['items']:
            like_dict = sanitize_like_dict(raw_like_dict)   
            like, created = Like.objects.get_or_create(
                object=like_dict['object'], 
                author=like_dict['author'],
                defaults=like_dict)
        
    except Exception as e:
        print("CRUD_likes exception : {}\n\n{}".format(type(e), str(e)))


"""
Update Authors
"""

def update_remote_authors(host: str, auth: str):
    """
    This will make an author API request to the host using auth to get the list of current authors on the remote note and updating our database accordingly

    args:
        host - The host url of the remote server
        auth - The authentication information to send to the server

    returns:
        foreign_ids - The list of foreign ids from the host
    """
    try:
        url = host + 'authors/'
        query = {'page': 1, 'size': 1000}
        res = requests.get(
            url,
            headers = {'Authorization': "Basic {}".format(
            auth), 'Accept': 'application/json'},
            params=query
        )
        if res.status_code not in range(200, 300):
            raise Exception(str(res.text))
        raw_author_dict_list = res.json()
        author_dict_list = []
        for raw_author_dict in raw_author_dict_list['items']:
            author_dict = sanitize_author_dict(raw_author_dict)
            if author_dict == None:
                continue
            author_dict_list.append(author_dict)
        CRUD_remote_authors(host, author_dict_list)
    except Exception as e:
        print("update_remote_authors exception : {}\n\n{}".format(type(e), str(e)))
        return []
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
        print("update_remote_authors exception : {}\n\n{}".format(type(e), str(e)))