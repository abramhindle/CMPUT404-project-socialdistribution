import requests

from service.models import Author
from service.services.team_10.helper_constants import AUTH


def is_author_remote(author: Author):
    pass


def get_author_id(author):
    author_guid = author.url.rsplit('/', 1)[-1]
    return author_guid


def get_remote(url):
    try:
        response = requests.get(url, headers=AUTH)
        response.close()
    except Exception as e:
        print("Got an exception of: %s", e)
        return None

    if response.status_code < 200 or response.status_code > 299:
        print("Got a status code of: %s", response.status_code)
        return None

    return response


def post_remote(url, request_json):
    try:
        response = requests.post(url, json=request_json, headers=AUTH)
        response.close()
    except Exception as e:
        print("Got an exception of: %s", e)
        return None  # just say not found

    if response.status_code < 200 or response.status_code > 299:
        print("Got a status code of: %s", response.status_code)
        return None
    return response
