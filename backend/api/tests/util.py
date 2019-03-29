import urllib
from ..models import Post, Category, AllowToView
import time


# return author id that is escaped
# input id should be the short id from author profile
def get_author_id(host, input_id, escaped):
    formated_id = "{}author/{}".format(host, str(input_id))
    if (escaped):
        formated_id = urllib.parse.quote(formated_id, safe='~()*!.\'')
    return formated_id


def create_mock_post(dict_input, author_profile):
    for category in dict_input["categories"]:
        Category.objects.get_or_create(name=category)

    for author in dict_input["visibleTo"]:
        AllowToView.objects.get_or_create(user_id=author)

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
    post.visibleTo.set(dict_input["visibleTo"])

    time.sleep(0.0001)
    return post


def assert_post(output, expected_post, author_profile):
    for key in expected_post.keys():
        if key == "category" or key == "visibleTo":
            assert len(output[key]) == len(expected_post[key])
            for expected_ele in expected_post[key]:
                assert expected_ele in output[key]
        elif key != "id" and key != "author" and key != "published" and key != "source" and key != "origin":
            assert output[key] == expected_post[key]
    # assert author part

    assert output["author"]["host"] == author_profile.host
    assert output["author"]["displayName"] == author_profile.displayName
    assert output["author"]["github"] == author_profile.github

    expected_id = "{}author/{}".format(author_profile.host, author_profile.id)
    assert output["author"]["id"] == expected_id
    assert output["author"]["url"] == expected_id

# custom assert for comments on a post
# Tests parts of the python dict struct such as author dict and comment/contentType
def assert_comments(post, author, expected_comment):
    comments = post["comments"]
    for i in range(len(comments)):
        assert (comments[i]["author"]["id"] == expected_comment[i]["author"]["id"])
        # assert (comments[i]["url"] == expected_comment[i]["author"]["url"])
        assert (comments[i]["author"]["host"] == expected_comment[i]["author"]["host"])
        assert (comments[i]["author"]["displayName"] == expected_comment[i]["author"]["displayName"])
        assert (comments[i]["author"]["github"] == expected_comment[i]["author"]["github"])
        assert (comments[i]["comment"] == expected_comment[i]["comment"])
        assert (comments[i]["contentType"] == expected_comment[i]["contentType"])

def assert_post_response(response, expected_output, expected_author):
    assert (response.status_code == 200)
    assert (response.data["query"] == expected_output["query"])
    assert (response.data["count"] == expected_output["count"])

    assert (len(response.data["posts"]) == len(expected_output["posts"]))
    for i in range(len(expected_output["posts"])):
        assert_post(response.data["posts"][i], expected_output["posts"][i], expected_author[i])
