from rest_framework.test import APITestCase
from webserver.tests.helpers import (
    create_local_author, 
    create_local_post,
    create_remote_node
)
from rest_framework import status
from webserver.models import Comment, Inbox, RemoteAuthor
from responses import matchers
import responses
import uuid
from webserver.utils import join_urls

class CommentsTestCase(APITestCase):
    def test_local_author_can_comment_on_local_post(self):
        author_1 = create_local_author()
        post = create_local_post(author_1)
        author_2 = create_local_author(username="another_author", display_name="another_author")
        
        # author_2 comments on author_1's post
        url = f'/api/authors/{author_1.id}/inbox/'
        self.client.force_authenticate(user=author_2)
        payload = {
            "type": "comment",
            "author": {
                "id": f"{author_2.id}",
                "url": f"http://127.0.0.1:5054/authors/{author_2.id}"
            },
            "post": {
                "id": f"{post.id}",
                "author": {
                    "id": f"{author_1.id}",
                    "url": f"http://127.0.0.1:5054/authors/{author_1.id}"
                }
            },
            "comment": "Awesome post!",
            "content_type": "text/plain",
        }
        response = self.client.post(url, data=payload, format="json")
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(1, Comment.objects.count())
        self.assertEqual(1, Inbox.objects.count())
        
        comment = Comment.objects.first()
        self.assertEqual(author_2, comment.author)
        self.assertEqual(post, comment.post)
        self.assertEqual("Awesome post!", comment.comment)
        
        inbox = Inbox.objects.first()
        self.assertEqual(author_1, inbox.target_author)
        self.assertEqual(comment, inbox.comment)

    @responses.activate
    def test_local_author_can_comment_on_remote_post_from_team14(self):
        author_1 = create_local_author()
        node = create_remote_node(team=14)
        remote_author_id = uuid.uuid4()
        remote_author_url = join_urls(node.api_url, f"authors/{remote_author_id}")
        remote_post_id = uuid.uuid4()
        remote_author_json = {
            "id": f"{remote_author_id}",
            "url": remote_author_url,
            "display_name": "remote_author",
            "profile_image": "",
            "github_handle": "",
        }
        
        request_payload = {
            "type": "comment",
            "author": {
                "id": f"{author_1.id}",
                "url": f"http://127.0.0.1:5054/authors/{author_1.id}"
            },
            "post": {
                "id": f"{remote_post_id}",
                "author": {
                    "id": f"{remote_author_id}",
                    "url": remote_author_url
                }
            },
            "comment": "Awesome post!",
            "content_type": "text/plain",
        }
        
        
        responses.add(
            responses.GET,
            remote_author_url,
            json=remote_author_json,
            status=200,
        )
        
        expected_remote_payload = request_payload
        responses.add(
            responses.POST,
            join_urls(remote_author_url, "inbox", ends_with_slash=True),
            match=[
                matchers.json_params_matcher(expected_remote_payload),
            ],
            status=201,
        )
        
        url = f'/api/authors/{remote_author_id}/inbox/'
        self.client.force_authenticate(user=author_1)
        
        response = self.client.post(url, data=request_payload, format="json")
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(0, Comment.objects.count())
        self.assertEqual(0, Inbox.objects.count())
    
    def test_remote_author_can_comment_on_local_post(self):
        author_1 = create_local_author()
        post = create_local_post(author_1)
        node = create_remote_node(team=14)
        remote_author_id = uuid.uuid4()
        remote_author_url = join_urls(node.api_url, f"authors/{remote_author_id}")
        
        request_payload = {
            "type": "comment",
            "author": {
                "id": f"{remote_author_id}",
                "url": remote_author_url,
            },
            "post": {
                "id": f"{post.id}",
                "author": {
                    "id": f"{author_1.id}",
                    "url": f"http://127.0.0.1:5054/authors/{author_1.id}"
                }
            },
            "comment": "Awesome post!",
            "content_type": "text/plain",
        }
        url = f'/api/authors/{author_1.id}/inbox/'
        self.client.force_authenticate(user=node.user)
        response = self.client.post(url, data=request_payload, format="json")
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(1, Comment.objects.count())
        self.assertEqual(1, Inbox.objects.count())
        self.assertEqual(1, RemoteAuthor.objects.count())
        
        remote_author = RemoteAuthor.objects.first()
        self.assertEqual(remote_author_id, remote_author.id)
        self.assertEqual(node, remote_author.node)
        
        comment = Comment.objects.first()
        self.assertEqual(remote_author, comment.remote_author)
        self.assertEqual(post, comment.post)
        
        inbox = Inbox.objects.first()
        self.assertEqual(author_1, inbox.target_author)
        self.assertEqual(comment, inbox.comment)
    
    def test_get_comment_inbox_from_local_author(self):
        author_1 = create_local_author()
        author_2 = create_local_author(username="author_2", display_name="author_2")
        post = create_local_post(author_1)
        comment = post.comment_set.create(author=author_2, comment="Awesome post!")
        Inbox.objects.create(target_author=author_1, comment=comment)
        
        url = f'/api/authors/{author_1.id}/inbox/'
        self.client.force_authenticate(user=author_1)
        response = self.client.get(url)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        
        expected_response = [
            {
                "type": "comment",
                "comment": "Awesome post!",
                "content_type": "text/plain",
                "created_at": comment.created_at.isoformat().replace("+00:00", "Z"),
                "id": f"http://testserver/api/authors/{author_1.id}/posts/{post.id}/comments/{comment.id}/",
                "author": {
                    "id": f"{author_2.id}",
                    "url": f"http://testserver/api/authors/{author_2.id}/",
                    "display_name": "author_2",
                    "profile_image": "",
                    "github_handle": "",
                }
            }
        ]
        self.assertEqual(expected_response, response.data)
    
    def test_get_comment_inbox_from_remote_author(self):
        pass
    
    def test_comments_are_returned_with_public_posts(self):
        author_1 = create_local_author()
        author_2 = create_local_author(username="author_2", display_name="author_2")
        post = create_local_post(author_1)
        comment = post.comment_set.create(author=author_2, comment="Awesome post!")
        
        url = f'/api/authors/{author_1.id}/posts/{post.id}/'
        self.client.force_authenticate(user=author_2)
        response = self.client.get(url)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(1, response.data["count"])
        self.assertEqual(f"http://testserver/api/authors/{author_1.id}/posts/{post.id}/comments", response.data["comments"])
        expected_comments_src = {
            "type": "comments",
            "page": 1,
            "size": 1,
            "comments": [
                {
                    "comment": "Awesome post!",
                    "content_type": "text/plain",
                    "created_at": comment.created_at.isoformat().replace("+00:00", "Z"),
                    "id": f"http://testserver/api/authors/{author_1.id}/posts/{post.id}/comments/{comment.id}/",
                    "author": {
                        "id": f"{author_2.id}",
                        "url": f"http://testserver/api/authors/{author_2.id}/",
                        "display_name": "author_2",
                        "profile_image": "",
                        "github_handle": "",
                    }
                }
            ]
        }
        self.assertEqual(expected_comments_src, response.data["comments_src"])
    
    def test_comments_are_not_returned_with_friends_posts(self):
        pass

    def test_comments_are_returned_with_friends_posts_if_request_user_is_the_post_author(self):
        pass
    
    @responses.activate
    def test_get_comments_on_local_post(self):
        author_1 = create_local_author()
        author_2 = create_local_author(username="author_2", display_name="author_2")
        node = create_remote_node(team=14)
        remote_author_id = uuid.uuid4()
        remote_author = RemoteAuthor.objects.create(id=remote_author_id, node=node)
        post = create_local_post(author_1)
        comment_1 = post.comment_set.create(author=author_2, comment="Awesome post!")
        comment_2 = post.comment_set.create(remote_author=remote_author, comment="Great post man!")
        
        remote_author_json = {
            "id": f"{remote_author_id}",
            "url": remote_author.get_absolute_url(),
            "display_name": "Jake",
            "profile_image": "",
            "github_handle": "",
        }
        responses.add(
            responses.GET,
            remote_author.get_absolute_url(),
            json=remote_author_json,
            status=200,
        )
        
        url = f'/api/authors/{author_1.id}/posts/{post.id}/comments/'
        self.client.force_authenticate(user=author_1)
        response = self.client.get(url)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        
        converted_remote_author_json = remote_author_json
        expected_response = [
            {
                "comment": "Great post man!",
                "content_type": "text/plain",
                "created_at": comment_2.created_at.isoformat().replace("+00:00", "Z"),
                "id": f"http://testserver/api/authors/{author_1.id}/posts/{post.id}/comments/{comment_2.id}/",
                "author": converted_remote_author_json,
            },
            {
                "comment": "Awesome post!",
                "content_type": "text/plain",
                "created_at": comment_1.created_at.isoformat().replace("+00:00", "Z"),
                "id": f"http://testserver/api/authors/{author_1.id}/posts/{post.id}/comments/{comment_1.id}/",
                "author": {
                    "id": f"{author_2.id}",
                    "url": f"http://testserver/api/authors/{author_2.id}/",
                    "display_name": "author_2",
                    "profile_image": "",
                    "github_handle": "",
                }
            }
        ]
        self.assertEqual(expected_response, response.data)
    
    @responses.activate
    def test_get_comments_on_remote_post_from_team14(self):
        local_author = create_local_author()
        node = create_remote_node(team=14)
        remote_author_id = uuid.uuid4()
        remote_author = RemoteAuthor.objects.create(id=remote_author_id, node=node)
        remote_post_id = uuid.uuid4()
        remote_author_2_id = uuid.uuid4()
        remote_author_3_id = uuid.uuid4()
        
        remote_comments_json = [
            {
                "comment": "Great post man!",
                "content_type": "text/plain",
                "created_at": "2020-04-01T00:00:00Z",
                "id": f"http://testserver/api/authors/{remote_author_id}/posts/{remote_post_id}/comments/1/",
                "author": {
                    "id": f"{remote_author_2_id}",
                    "url": f"http://testserver/api/authors/{remote_author_2_id}/",
                    "display_name": "author_2",
                    "profile_image": "",
                    "github_handle": "",
                },
            },
            {
                "comment": "Awesome post!",
                "content_type": "text/plain",
                "created_at": "2020-04-02T00:00:00Z",
                "id": f"http://testserver/api/authors/{remote_author_id}/posts/{remote_post_id}/comments/2/",
                "author": {
                    "id": f"{remote_author_3_id}",
                    "url": f"http://testserver/api/authors/{remote_author_3_id}/",
                    "display_name": "author_3",
                    "profile_image": "",
                    "github_handle": "",
                }
            }
        ]
        responses.add(
            responses.GET,
            join_urls(node.api_url, f"authors/{remote_author_id}/posts/{remote_post_id}/comments", ends_with_slash=True),
            json=remote_comments_json,
            status=200,
        )
        
        url = f'/api/authors/{remote_author_id}/posts/{remote_post_id}/comments/'
        self.client.force_authenticate(user=local_author)
        response = self.client.get(url)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        
        converted_remote_comments_json = remote_comments_json
        self.assertEqual(converted_remote_comments_json, response.data)
