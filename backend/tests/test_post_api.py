from django.conf import settings
from backend.models import Post, Host, User
from backend.permissions import *

import pytest
import json


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
        assert response.data["size"] == 50

        assert response.data["posts"] is not None
        assert len(response.data["posts"]) == 1
        assert response.data["posts"][0]["title"] == "post title"
        assert response.data["posts"][0]["content"] == "post content"

        assert response.data["posts"][0]["author"] is not None
        assert response.data["posts"][0]["author"]["displayName"] == test_user.username
        assert response.data["posts"][0]["author"]["github"] == test_user.githubUrl

    def test_create_post(self, client, test_user):
        test_post_title = "testpost001"
        test_post_content = "testposttitle001"
        post_body_1 = json.dumps({
            "title": test_post_title,
            "content": test_post_content,
            "visibility": PUBLIC
        })

        response = client.post('/author/posts', data=post_body_1,
                               content_type='application/json', charset='UTF-8')
        assert response.status_code == 401

        # Post should only be created after user is authenticated
        client.force_login(test_user)
        response = client.post('/author/posts', data=post_body_1,
                               content_type='application/json', charset='UTF-8')
        assert response.status_code == 201

    def test_delete_post(self, client, test_user):
        # Create a post used to test the delete
        test_post = Post.objects.create(
            author=test_user, title="post title", content="post content")
        test_post_id = test_post.postId
        # Create another user
        test_user_non_author = User.objects.create_user(
            username='testuser002', password='ualberta!')

        response = client.delete('/posts/{}/'.format(test_post_id))
        assert response.status_code == 401

        # user other than post owner shouldn't be able to delete the post
        client.force_login(test_user_non_author)
        response = client.delete('/posts/{}/'.format(test_post_id))
        assert response.status_code == 403

        client.logout()
        client.force_login(test_user)
        response = client.delete('/posts/{}/'.format(test_post_id))
        assert response.status_code == 204
        assert not Post.objects.filter(postId=test_post_id).exists()

    def test_get_visible_post(self, client, test_user, test_host):
        test_user_no_access = User.objects.create_user(
            username='testuser003', password='ualberta!', host=test_host)
        test_user_with_access = User.objects.create_user(
            username='testuser004', password='ualberta!', host=test_host)

        test_post = Post.objects.create(
            author=test_user, title="post title", content="post content", visibility=PRIVATE, visibleTo=[test_user_with_access.get_full_user_id()])

        client.force_login(test_user_no_access)
        response = client.get('/author/posts')
        assert response.status_code == 200
        assert response.data["query"] == "posts"
        assert response.data["count"] == 0
        assert response.data["posts"] is not None
        assert len(response.data["posts"]) == 0
        client.logout()

        client.force_login(test_user_with_access)
        response = client.get('/author/posts')
        assert response.status_code == 200
        assert response.data["query"] == "posts"
        assert response.data["count"] >= 0
        assert response.data["posts"] is not None
        assert len(response.data["posts"]) > 0
        assert response.data["posts"][0]["content"] == test_post.content
        client.logout()
