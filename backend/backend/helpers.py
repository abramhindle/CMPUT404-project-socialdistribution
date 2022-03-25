from django import db
from concurrent.futures import ThreadPoolExecutor
from authors.models import Author
from authors.serializers import AuthorSerializer
from urllib import parse
from nodes.models import Node
from requests.auth import HTTPBasicAuth
import requests as r
from django.conf import settings


def get_node(url):
    p = parse.urlparse(url)
    hostname = f"{p.scheme}://{p.hostname}"
    nodes = Node.objects.filter(host__contains=hostname)
    return nodes[0] if len(nodes) > 0 else None


def get(url, headers=None, params=None):
    if headers is not None and "Authorization" in headers:
        return r.get(url, headers=headers, params=params)
    node = get_node(url)
    return r.get(url, headers=headers, params=params, auth=HTTPBasicAuth(username=node.outbound_username, password=node.outbound_password)) if node is not None else None


def post(url, data, headers=None):
    if headers is not None and "Authorization" in headers:
        return r.post(url, data=data, headers=headers)
    node = get_node(url)
    return r.post(url, data=data, headers=headers, auth=HTTPBasicAuth(username=node.outbound_username, password=node.outbound_password)) if node is not None else None


def delete(url, headers=None):
    if headers is not None and "Authorization" in headers:
        return r.delete(url, headers=headers)
    node = get_node(url)
    return r.delete(url, headers=headers, auth=HTTPBasicAuth(username=node.outbound_username, password=node.outbound_password)) if node is not None else None


def patch(url, data, headers=None):
    if headers is not None and "Authorization" in headers:
        return r.patch(url, data=data, headers=headers)
    node = get_node(url)
    return r.patch(url, data=data, headers=headers, auth=HTTPBasicAuth(username=node.outbound_username, password=node.outbound_password)) if node is not None else None


def put(url, data, headers=None):
    if headers is not None and "Authorization" in headers:
        return r.put(url, data=data, headers=headers)
    node = get_node(url)
    return r.put(url, data=data, headers=headers, auth=HTTPBasicAuth(username=node.outbound_username, password=node.outbound_password)) if node is not None else None


def get_author(author, headers=None):
    hostname = get_hostname(author)
    if hostname in settings.DOMAIN:
        authors = Author.objects.filter(id__contains=author)
        return AuthorSerializer(authors[0]).data if len(authors) > 0 else {"error": "Author Not Found!"}
    response = get(author, headers)
    return response.json() if response is not None and response.status_code == 200 else {"error": "Author Not Found!"}


def get_author_list(authors, headers=None):
    # Fetch Local Authors
    local_authors = [get_author(author) for author in authors if get_hostname(author) in settings.DOMAIN]

    # Fetch Remote Authors
    db.connections.close_all()
    remote_authors = [author for author in authors if get_hostname(author) not in settings.DOMAIN]
    with ThreadPoolExecutor(max_workers=1) as executor:
        future = executor.map(lambda author: get_author(author), remote_authors)

    # Sort And Return Authors
    return local_authors + [author for author in future]


def get_authors(host: str, headers=None):
    response = get(f"{host.rstrip('/')}/authors/", headers)
    return response.json() if response is not None and response.status_code == 200 else {"error": "Cannot Connect To Host!"}


def get_hostname(url):
    p = parse.urlparse(url)
    return f"{p.scheme}://{p.hostname}"


def extract_local_id(author):
    return author["id"].split("/authors/")[1].rstrip("/")


def extract_inbox_url(author):
    host = author["host"]
    if host == "http://squawker-cmput404.herokuapp.com/":
        return f"{host}api/authors/{extract_local_id(author)}/inbox/"
    return f"{host}api/authors/{extract_local_id(author)}/inbox/"


def extract_profile_image(author):
    return author["profileImage"] if "http://" in author["profileImage"] else "https://cdn.pixabay.com/photo/2016/08/08/09/17/avatar-1577909_1280.png"


def extract_visibility(remote_post):
    host = remote_post["id"]
    if host == "http://squawker-cmput404.herokuapp.com/":
        return remote_post["visibility"].upper() if remote_post["visibility"] == "public" or remote_post["visibility"] == "friends" else remote_post["visibility"]
    return remote_post["visibility"]


def extract_remote_id(url):
    host = get_hostname(url)
    if host.rstrip("/") == "http://squawker-cmput404.herokuapp.com/".rstrip("/"):
        return f"{host}/api/authors/{url.split('/authors/')[1]}/"
    return url


def extract_content_type(remote_post):
    host = get_hostname(remote_post["id"])
    if host.rstrip("/") == "http://squawker-cmput404.herokuapp.com/".rstrip("/"):
        return remote_post["content_type"]
    return remote_post["contentType"]


def extract_posts_url(author):
    host = author["host"]
    if host == "http://squawker-cmput404.herokuapp.com/":
        return f"{host}api/authors/{extract_local_id(author)}/posts/"
    return f"{host}api/authors/{extract_local_id(author)}/posts/"
