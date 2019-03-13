import urllib
from ..models import Post
import time

# return author id that is escaped
def get_author_id(host, input_id, escaped):
    formated_id = "{}author/{}".format(host, str(input_id))
    if(escaped):
        formated_id = urllib.parse.quote(formated_id, safe='~()*!.\'')
    return formated_id

def create_mock_post(dict_input, author_profile):
    post = Post.objects.create(title=dict_input["title"],
                                source=dict_input["source"],
                                origin=dict_input["origin"],
                                description=dict_input["description"],
                                contentType=dict_input["contentType"],
                                content=dict_input["content"],
                                author=author_profile,
                                visibility=dict_input["visibility"],
                                unlisted=dict_input["unlisted"])
    post.categories.set(dict_input["categories"])
    post.visibleTo.set(dict_input["visibleTo"
                        ])

    time.sleep(0.0001)
    return post

def assert_post(output, expected_post, author_profile):
    for key in expected_post.keys():
        if key != "id" and key != "author" and key != "published":
            assert output[key] == expected_post[key]
    # assert author part
    for key in ["host", "displayName", "github"]:
        assert output["author"][key] == expected_post["author"][key]
    expected_id = "{}author/{}".format(author_profile.host, author_profile.id)
    assert output["author"]["id"] == expected_id
    assert output["author"]["url"] == expected_id

def assert_post_response(response, expected_output, expected_author):
    assert(response.status_code == 200)
    assert(response.data["query"] == expected_output["query"])
    assert(response.data["count"] == expected_output["count"])

    assert(len(response.data["posts"]) == len(expected_output["posts"]))
    for i in range(len(expected_output["posts"])):
        assert_post(response.data["posts"][i], expected_output["posts"][i], expected_author[i])
