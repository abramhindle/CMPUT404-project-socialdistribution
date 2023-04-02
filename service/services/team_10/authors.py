from service.models import Author
from service.services.team_10.followers import get_followers
from service.services.team_10.helper_constants import HOST, get_or_create_author
from service.services.remote_helpers import get_author_id, get_remote

def get_single_author(author):
    author_guid = get_author_id(author)
    url = HOST + "api/authors/" + author_guid
    response = get_remote(url)

    if not response:
        return None

    return get_or_create_author(response.json(), author.host)


def get_multiple_authors(page=None, size=None):  # no paging yet
    url = HOST + "api/authors/"
    response = get_remote(url)

    if not response:
        return None

    response_json = response.json()

    authors = list()

    for author in response_json["items"]:
        author = get_or_create_author(author, HOST)
        authors.append(author)

    return authors