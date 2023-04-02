from service.services.team_10.helper_constants import HOST
from service.services.remote_helpers import get_remote


def get_comments(author, post):
    author_guid = author.url.rsplit('/', 1)[-1]
    post_guid = post.source.rsplit('/', 1)[-1]

    url = HOST + "api/authors/" + author_guid + "/posts/" + post_guid + "/comments/"

    response = get_remote(url)
    if not response:
        return None

    response_json = response.json()

    response_json["items"] = response_json.pop("items")

    # we CANNOT Store copies of their comments -> no way to differentiate, only one ID field
    for comment in response_json["items"]:
        comment["author"] = author.toJSON()
        try:
            comment["comment"] = comment.pop("content")
        except KeyError:
            print(comment["comment"])
    return response_json