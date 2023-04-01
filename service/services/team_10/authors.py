from django.core.exceptions import ObjectDoesNotExist

from service.models import Author
from service.services.team_10.helper_constants import HOST
from service.services.remote_helpers import get_author_id, get_remote


def get_or_create_author(author_json, hostname=HOST):
    try:
        # update old -> don't change host_url or id
        old_author = Author.objects.get(url=author_json["id"])

        old_author.github = author_json["github"]
        old_author.displayName = author_json["displayName"]
        old_author.save()

        return old_author

    except ObjectDoesNotExist:
        # create new
        new_author = Author()
        # new_author._id = f"{settings.DOMAIN}/authors/{author_json['id']}"  # we use the GUID sent to us
        new_author.github = author_json["github"]
        new_author.displayName = author_json["displayName"]
        new_author.url = author_json["id"]
        new_author.host = hostname
        new_author.save()

        return new_author


def get_single_author(author):
    author_guid = get_author_id(author)
    url = HOST + "api/authors/" + author_guid
    response = get_remote(url)

    if not response:
        return None

    return get_or_create_author(response.json(), author.host)


def get_multiple_authors(page, size):  # no paging yet
    url = HOST + "api/authors/"
    response = get_remote(url)

    if not response:
        return None

    response_json = response.json()

    for author in response_json["items"]:
        get_or_create_author(author, HOST)
