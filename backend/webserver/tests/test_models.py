from django.test import TestCase
from webserver.models import Author, Node, Post, RemoteAuthor, Follow
from responses import matchers
import responses
import uuid
from asgiref.sync import sync_to_async
from aioresponses import aioresponses   # https://pypi.org/project/aioresponses/
from unittest.mock import MagicMock

class NodeTestCase(TestCase):
    def test_get_node_with_url(self):
        node_user_1 = Author.objects.create(username="node_user_1", display_name="node_user_1", 
                                            password="password1", is_remote_user=True)
        node_user_2 = Author.objects.create(username="node_user_2", display_name="node_user_2", 
                                            password="password2", is_remote_user=True)
        node_1 = Node.objects.create(api_url="https://social-distribution-1.herokuapp.com/api", user=node_user_1,
                                     auth_username="team14", auth_password="password-team14")
        Node.objects.create(api_url="https://social-distribution-2.herokuapp.com/api", user=node_user_2,
                            auth_username="team14-2", auth_password="password-team14-2")
        search_url = "https://social-distribution-1.herokuapp.com/api/authors/123/"
        result = Node.objects.get_node_with_url(search_url)
        self.assertEqual(node_1, result)

    def test_get_node_with_url_raises_DoesNotExist(self):
        with self.assertRaises(Node.DoesNotExist):
            Node.objects.get_node_with_url("https://social-distribution-1.herokuapp.com/api")


class PostTestCase(TestCase):
    @responses.activate
    def test_send_post_to_multiple_remote_followers_in_team14(self):
        local_author = Author.objects.create(username="local_author", display_name="local_author")
        node_user = Author.objects.create(username="node_user", display_name="node_user", is_remote_user=True)
        node = Node.objects.create(api_url="https://social-distribution-1.herokuapp.com/api", user=node_user,
                                   auth_username="team14", auth_password="password-team14", team=14)
        remote_author = RemoteAuthor.objects.create(id=uuid.uuid4(), node=node)
        remote_author_2 = RemoteAuthor.objects.create(id=uuid.uuid4(), node=node)
        Follow.objects.create(remote_follower=remote_author, followee=local_author)
        Follow.objects.create(remote_follower=remote_author_2, followee=local_author)
        
        post = Post.objects.create(
            author=local_author,
            title="Test Post",
            description="Testing post",
            source="source",
            origin="origin",
            unlisted=False,
            visibility = "FRIENDS"
        )
        
        responses.add(
            responses.POST,
            f"https://social-distribution-1.herokuapp.com/api/authors/{remote_author.id}/inbox/",
            match=[matchers.json_params_matcher({
                "type": "post",
                "post": {
                    "id": f"{post.id}",
                    "author": {
                        "id": f"{local_author.id}",
                        "url": f"http://testserver/api/authors/{local_author.id}/",
                    }
                }
            })],
            status=201,
        )
        responses.add(
            responses.POST,
            f"https://social-distribution-1.herokuapp.com/api/authors/{remote_author_2.id}/inbox/",
            match=[matchers.json_params_matcher({
                "type": "post",
                "post": {
                    "id": f"{post.id}",
                    "author": {
                        "id": f"{local_author.id}",
                        "url": f"http://testserver/api/authors/{local_author.id}/",
                    }
                }
            })],
            status=201,
        )
        mock_request = MagicMock()
        mock_request.build_absolute_uri.return_value = f"http://testserver/api/authors/{local_author.id}/"
        success = post.send_to_followers(mock_request)
        mock_request.build_absolute_uri.assert_called_with(f"/api/authors/{local_author.id}/")
        self.assertTrue(success)
    
    @responses.activate
    def test_send_post_to_multiple_remote_followers_in_team10(self):
        local_author = Author.objects.create(username="local_author", display_name="local_author")
        node_user = Author.objects.create(username="node_user", display_name="node_user", is_remote_user=True)
        node = Node.objects.create(api_url="https://social-distribution-1.herokuapp.com/api", user=node_user,
                                   auth_username="team14", auth_password="password-team14", team=10)
        remote_author = RemoteAuthor.objects.create(id=uuid.uuid4(), node=node)
        remote_author_2 = RemoteAuthor.objects.create(id=uuid.uuid4(), node=node)
        Follow.objects.create(remote_follower=remote_author, followee=local_author)
        Follow.objects.create(remote_follower=remote_author_2, followee=local_author)
        
        post = Post.objects.create(
            author=local_author,
            title="Test Post",
            description="Testing post",
            source="source",
            origin="origin",
            unlisted=False,
            visibility = "FRIENDS",
            content_type ="text/plain"
        )
        
        responses.add(
            responses.POST,
            f"https://social-distribution-1.herokuapp.com/api/authors/{remote_author.id}/inbox/",
            match=[matchers.json_params_matcher({
                "author":{
                    "url": f"http://testserver/api/authors/{local_author.id}/",
                    "id": f"{local_author.id}",
                    "host":"http://testserver/",
                    "displayName": "local_author",
                    "profileImage": "",
                    "github": ""
                },
                "title": post.title,
                "description": post.description,
                "visibility": post.visibility.lower(),
                "source": post.source,
                "origin": post.origin,
                "categories": ["post"],
                "contentType": post.content_type,
                "unlisted": post.unlisted,
                "count": "0",
                "comments":"",
                "published": f"{post.created_at}"
            })],
            status=201,
        )
        responses.add(
            responses.POST,
            f"https://social-distribution-1.herokuapp.com/api/authors/{remote_author_2.id}/inbox/",
            match=[matchers.json_params_matcher({
                "author":{
                    "url": f"http://testserver/api/authors/{local_author.id}/",
                    "id": f"{local_author.id}",
                    "host":"http://testserver/",
                    "displayName": "local_author",
                    "profileImage": "",
                    "github": ""
                },
                "title": post.title,
                "description": post.description,
                "visibility": post.visibility.lower(),
                "source": post.source,
                "origin": post.origin,
                "categories": ["post"],
                "contentType": post.content_type,
                "unlisted": post.unlisted,
                "count": "0",
                "comments":"",
                "published": f"{post.created_at}"
            })],
            status=201,
        )
        mock_request = MagicMock()
        mock_request.build_absolute_uri.return_value = f"http://testserver/api/authors/{local_author.id}/"
        success = post.send_to_followers(mock_request)
        mock_request.build_absolute_uri.assert_called_with(f"/api/authors/{local_author.id}/")
        self.assertTrue(success)
    
    @responses.activate
    def test_send_post_to_all_remote_authors_on_team14_node(self):
        local_author = Author.objects.create(username="local_author", display_name="local_author")
        node_user = Author.objects.create(username="node_user", display_name="node_user", is_remote_user=True)
        node = Node.objects.create(api_url="https://social-distribution-1.herokuapp.com/api", user=node_user,
                                   auth_username="team14", auth_password="password-team14", team=14)
        remote_author_id = uuid.uuid4()

        post = Post.objects.create(
            author=local_author,
            title="Test Post",
            description="Testing post",
            source="source",
            origin="origin",
            unlisted=False,
            visibility = "PUBLIC"
        )
        
        remote_author_json = {
            "url": f"https://social-distribution-1.herokuapp.com/api/authors/{remote_author_id}",
            "id": f"{remote_author_id}",
            "display_name": "Jake",
            "profile_image": "",
            "github_handle": ""
        }
        responses.add(
            responses.GET,
            f"https://social-distribution-1.herokuapp.com/api/authors",
            json=[remote_author_json],
            status=200,
        )
        responses.add(
            responses.POST,
            f"https://social-distribution-1.herokuapp.com/api/authors/{remote_author_id}/inbox/",
            match=[matchers.json_params_matcher({
                "type": "post",
                "post": {
                    "id": f"{post.id}",
                    "author": {
                        "id": f"{local_author.id}",
                        "url": f"http://testserver/api/authors/{local_author.id}/"
                    }
                }
            })],
            status=201,
        )
        mock_request = MagicMock()
        mock_request.build_absolute_uri.return_value = f"http://testserver/api/authors/{local_author.id}/"
        sucess = post.send_to_all_authors(mock_request)
        mock_request.build_absolute_uri.assert_called_with(f"/api/authors/{local_author.id}/")
        self.assertTrue(sucess)

    @responses.activate
    def test_send_post_to_all_remote_authors_on_team10_node(self):
        local_author = Author.objects.create(username="local_author", display_name="local_author")
        node_user = Author.objects.create(username="node_user", display_name="node_user", is_remote_user=True)
        node = Node.objects.create(api_url="https://social-distribution-1.herokuapp.com/api", user=node_user,
                                   auth_username="team10", auth_password="password-team10", team=10)
        remote_author_id = uuid.uuid4()

        post = Post.objects.create(
            author=local_author,
            title="Test Post",
            description="Testing post",
            source="source",
            origin="origin",
            unlisted=False,
            visibility = "PUBLIC",
            content_type = "text/plain",
        )
       
        remote_author_json = {
            "type":"author",
            "url": f"https://social-distribution-1.herokuapp.com/api/authors/{remote_author_id}/",
            "id": f"{remote_author_id}",
            "host":"",
            "displayName": "Jake",
            "profileImage": "",
            "github": ""
        }
        responses.add(
            responses.GET,
            f"https://social-distribution-1.herokuapp.com/api/authors",
            json={"type":"author","items":[remote_author_json]},
            status=200,
        )
        responses.add(
            responses.POST,
            f"https://social-distribution-1.herokuapp.com/api/authors/{remote_author_id}/inbox/",
            match=[matchers.json_params_matcher({
                "author":{
                    "url": f"http://testserver/api/authors/{local_author.id}/",
                    "id": f"{local_author.id}",
                    "host":"http://testserver/",
                    "displayName": "local_author",
                    "profileImage": "",
                    "github": ""
                },
                "title": post.title,
                "description": post.description,
                "visibility": post.visibility.lower(),
                "source": post.source,
                "origin": post.origin,
                "categories": ["post"],
                "contentType": post.content_type,
                "unlisted": post.unlisted,
                "count": "0",
                "comments":"",
                "published": f"{post.created_at}"     
            })],
            status=201,
        )
        
        mock_request = MagicMock()
        mock_request.build_absolute_uri.return_value = f"http://testserver/api/authors/{local_author.id}/"
        sucess = post.send_to_all_authors(mock_request)
        mock_request.build_absolute_uri.assert_called_with(f"/api/authors/{local_author.id}/")
        self.assertTrue(sucess)