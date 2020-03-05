from django.conf import settings
from backend.models import Post, Host

import pytest, json


@pytest.mark.django_db
class TestPostAPI:

    def test_get_post_by_id(self, client, test_user):
        test_post = Post.objects.create(
            author=test_user, title="post title", content="post content")
        test_post_id = test_post.postId

        response = client.get('/posts/{}/'.format(test_post_id))
        assert response.status_code == 200
        assert response.data["query"] == "posts"
        assert response.data["count"] == 1
        assert response.data["size"] == 1

        assert response.data["post"] is not None
        assert len(response.data["post"]) == 1
        assert response.data["post"][0]["title"] == "post title"
        assert response.data["post"][0]["content"] == "post content"

        assert response.data["post"][0]["author"] is not None
        assert response.data["post"][0]["author"]["displayName"] == test_user.username
        assert response.data["post"][0]["author"]["github"] == test_user.githubUrl

    def test_create_post(self, client, test_user):
        test_post_title = "testpost001"
        test_post_content = "testposttitle001"
        post_body_1 = json.dumps({
            "title": test_post_title,
            "content": test_post_content
        })
        
        response = client.post('/author/posts', data=post_body_1,
                           content_type='application/json', charset='UTF-8')
        assert response.status_code == 401

        # Post should only be created after user is authenticated
        client.force_login(test_user)
        response = client.post('/author/posts', data=post_body_1,
                           content_type='application/json', charset='UTF-8')
        assert response.status_code == 201





