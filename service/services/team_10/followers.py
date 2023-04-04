from service.services.team_10.helper_constants import HOST, get_or_create_author
from service.services.remote_helpers import get_author_id, get_remote

def get_followers(author):
    author_guid = get_author_id(author)

    url = HOST + "api/authors/" + author_guid + "/followers/"

    response = get_remote(url)
    if not response:
        return None

    response_json = response.json()
    authors = list()

    for follower in response_json["items"]:
        follower = get_or_create_author(follower, HOST)
        author.followers.add(follower)
        authors.append(follower.toJSON())

    author.save()

    return authors
