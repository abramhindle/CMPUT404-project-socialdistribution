from django.test import TestCase
from django.urls import reverse
import json

from rest_framework.test import APIClient

from tests.test_helper.auth_helper import AuthHelper

from apps.core.models import Author, User
from apps.posts.models import Post, Comment

from uuid import uuid4

class LikeViewTests(TestCase):
    def setUp(self):
        self.auth_helper = AuthHelper()
        self.auth_helper.setup()
        self.client = APIClient()
        self.auth_helper.authorize_client(self.client)

    # POSTs ####################

    def test_post_like(self):
        """
        should return inbox items with ids matching the created items
        """
        
        author = self.auth_helper.get_author()
        user = User.objects.create_user("username1")
        author2: Author = Author.objects.get(userId=user)

        post_data = {
            "type":"post",
            "title":"A post title about a post about web dev",
            "description":"This post discusses stuff -- brief",
            "contentType":f"{Post.ContentTypeEnum.MARKDOWN}",
            "author":{
                "type":"author",
                "id":f"{author.id}"
            },
            "visibility":f"{Post.VisibilityEnum.PUBLIC}",
            "unlisted":"false"
        }
        
        response = self.client.post(reverse('post_api:posts', kwargs={'author_id':author.id}), post_data, format="json")
        self.assertEqual(response.status_code, 201, f"expected 201. got: {response.status_code}")
        postId = json.loads(response.content)["data"]["id"]
        postIdFragment = postId.split("posts/")[1].rstrip("/")

        data = {
            "object": f"{postId}",
            "author":{
                "type":"author",
                "id":f"{author2.id}"
            },
        }

        response = self.client.post(reverse('likes_api:inbox_like', kwargs={'author_id':author.id}), data, format="json")
        self.assertEqual(response.status_code, 201, f"expected 201. got: {response.status_code}")
        dict_resp_data = json.loads(response.content)["data"]
        self.assertEqual(postId, dict_resp_data["object"], "returned item referenced wrong object!")
        self.assertEqual(dict_resp_data["author"]["id"], str(author2.id), "returned item referenced wrong author!")

        comment_data = {
            "type":"comment",
            "author":{
                "type":"author",
                "id":f"{author.id}"
            },
            "comment":"A Comment with words and markdown",
            "contentType":f"{Comment.ContentTypeEnum.MARKDOWN}"
        }

        response = self.client.post(reverse('post_api:comments', kwargs={'author_id':author.id, 'post_id':postIdFragment}), comment_data, format="json")
        self.assertEqual(response.status_code, 201, f"expected 201. got: {response.status_code}")

        commentId = json.loads(response.content)["data"]["id"]
        data = {
            "object": f"{commentId}",
            "author":{
                "type":"author",
                "id":f"{author2.id}"
            },
        }

        response = self.client.post(reverse('likes_api:inbox_like', kwargs={'author_id':author.id}), data, format="json")
        self.assertEqual(response.status_code, 201, f"expected 201. got: {response.status_code}")
        dict_resp_data = json.loads(response.content)["data"]
        self.assertEqual(commentId, dict_resp_data["object"], "returned item referenced wrong object!")
        self.assertEqual(dict_resp_data["author"]["id"], str(author2.id), "returned item referenced wrong author!")

    def test_post_like_access_levels(self):
        """
        should return 401 for anonymous users, 403 for non participants and the likee, and 201 for the liker and admins
        """
        
        password = "password"
        user = User.objects.create_user("username1", password=password)
        author: Author = Author.objects.get(userId=user)
        user2 = User.objects.create_user("username2", password=password)
        author2: Author = Author.objects.get(userId=user2)
        self.client.logout()
        self.client.login(username=user.username, password=password)

        post_data = {
            "type":"post",
            "title":"A post title about a post about web dev",
            "description":"This post discusses stuff -- brief",
            "contentType":f"{Post.ContentTypeEnum.MARKDOWN}",
            "author":{
                "type":"author",
                "id":f"{author.id}"
            },
            "visibility":f"{Post.VisibilityEnum.PUBLIC}",
            "unlisted":"false"
        }
        
        response = self.client.post(reverse('post_api:posts', kwargs={'author_id':author.id}), post_data, format="json")
        self.assertEqual(response.status_code, 201, f"expected 201. got: {response.status_code}")
        postId = json.loads(response.content)["data"]["id"]
        postIdFragment = postId.split("posts/")[1].rstrip("/")

        post_like_data = {
            "object": f"{postId}",
            "author":{
                "type":"author",
                "id":f"{author2.id}"
            },
        }

        comment_data = {
            "type":"comment",
            "author":{
                "type":"author",
                "id":f"{author.id}"
            },
            "comment":"A Comment with words and markdown",
            "contentType":f"{Comment.ContentTypeEnum.MARKDOWN}"
        }

        response = self.client.post(reverse('post_api:comments', kwargs={'author_id':author.id, 'post_id':postIdFragment}), comment_data, format="json")
        self.assertEqual(response.status_code, 201, f"expected 201. got: {response.status_code}")

        commentId = json.loads(response.content)["data"]["id"]
        
        comment_like_data = {
            "object": f"{commentId}",
            "author":{
                "type":"author",
                "id":f"{author2.id}"
            },
        }
        
        self.client.logout()
        # test anonymous user
        response = self.client.post(reverse('likes_api:inbox_like', kwargs={'author_id':author.id}), post_like_data, format="json")
        self.assertEqual(response.status_code, 401, f"expected 401. got: {response.status_code}")
        response = self.client.post(reverse('likes_api:inbox_like', kwargs={'author_id':author.id}), comment_like_data, format="json")
        self.assertEqual(response.status_code, 401, f"expected 401. got: {response.status_code}")
        # test non participant user
        nonParticipant = User.objects.create_user("nonParticipant", password=password)
        self.assertTrue(self.client.login(username=nonParticipant.username, password=password))
        response = self.client.post(reverse('likes_api:inbox_like', kwargs={'author_id':author.id}), post_like_data, format="json")
        self.assertEqual(response.status_code, 403, f"expected 403. got: {response.status_code}")
        response = self.client.post(reverse('likes_api:inbox_like', kwargs={'author_id':author.id}), comment_like_data, format="json")
        self.assertEqual(response.status_code, 403, f"expected 403. got: {response.status_code}")
        # test likee
        self.client.logout()
        self.assertTrue(self.client.login(username=user.username, password=password))
        response = self.client.post(reverse('likes_api:inbox_like', kwargs={'author_id':author.id}), post_like_data, format="json")
        self.assertEqual(response.status_code, 403, f"expected 403. got: {response.status_code}")
        response = self.client.post(reverse('likes_api:inbox_like', kwargs={'author_id':author.id}), comment_like_data, format="json")
        self.assertEqual(response.status_code, 403, f"expected 403. got: {response.status_code}")
        # test liker
        self.client.logout()
        self.assertTrue(self.client.login(username=user2.username, password=password))
        response = self.client.post(reverse('likes_api:inbox_like', kwargs={'author_id':author.id}), post_like_data, format="json")
        self.assertEqual(response.status_code, 201, f"expected 201. got: {response.status_code}")
        response = self.client.post(reverse('likes_api:inbox_like', kwargs={'author_id':author.id}), comment_like_data, format="json")
        self.assertEqual(response.status_code, 201, f"expected 201. got: {response.status_code}")
        # test admin
        self.client.logout()
        self.auth_helper.authorize_client(self.client)
        response = self.client.post(reverse('likes_api:inbox_like', kwargs={'author_id':author.id}), post_like_data, format="json")
        # 204's because author has already liked the post
        self.assertEqual(response.status_code, 204, f"expected 204. got: {response.status_code}")
        response = self.client.post(reverse('likes_api:inbox_like', kwargs={'author_id':author.id}), comment_like_data, format="json")
        # 204's because author has already liked the comment
        self.assertEqual(response.status_code, 204, f"expected 204. got: {response.status_code}")

    # should you be able to send things to your own inbox?
    def test_post_like_against_self(self):
        """
        should return inbox items with ids matching the created items. Should disallow friend request on self
        """
        
        author = self.auth_helper.get_author()

        post_data = {
            "type":"post",
            "title":"A post title about a post about web dev",
            "description":"This post discusses stuff -- brief",
            "contentType":f"{Post.ContentTypeEnum.MARKDOWN}",
            "author":{
                "type":"author",
                "id":f"{author.id}"
            },
            "visibility":f"{Post.VisibilityEnum.PUBLIC}",
            "unlisted":"false"
        }
        
        response = self.client.post(reverse('post_api:posts', kwargs={'author_id':author.id}), post_data, format="json")
        self.assertEqual(response.status_code, 201, f"expected 201. got: {response.status_code}")
        postId = json.loads(response.content)["data"]["id"]
        postIdFragment = postId.split("posts/")[1].rstrip("/")

        data = {
            "object": f"{postId}",
            "author":{
                "type":"author",
                "id":f"{author.id}"
            },
        }

        response = self.client.post(reverse('likes_api:inbox_like', kwargs={'author_id':author.id}), data, format="json")
        self.assertEqual(response.status_code, 201, f"expected 201. got: {response.status_code}")
        dict_resp_data = json.loads(response.content)["data"]
        self.assertEqual(postId, dict_resp_data["object"], "returned item referenced wrong object!")
        self.assertEqual(dict_resp_data["author"]["id"], str(author.id), "returned item referenced wrong author!")

        comment_data = {
            "type":"comment",
            "author":{
                "type":"author",
                "id":f"{author.id}"
            },
            "comment":"A Comment with words and markdown",
            "contentType":f"{Comment.ContentTypeEnum.MARKDOWN}"
        }

        response = self.client.post(reverse('post_api:comments', kwargs={'author_id':author.id, 'post_id':postIdFragment}), comment_data, format="json")
        self.assertEqual(response.status_code, 201, f"expected 201. got: {response.status_code}")

        commentId = json.loads(response.content)["data"]["id"]

        data = {
            "object": f"{commentId}",
            "author":{
                "type":"author",
                "id":f"{author.id}"
            },
        }

        response = self.client.post(reverse('likes_api:inbox_like', kwargs={'author_id':author.id}), data, format="json")
        self.assertEqual(response.status_code, 201, f"expected 201. got: {response.status_code}")
        dict_resp_data = json.loads(response.content)["data"]
        self.assertEqual(commentId, dict_resp_data["object"], "returned item referenced wrong object!")
        self.assertEqual(dict_resp_data["author"]["id"], str(author.id), "returned item referenced wrong author!")

    def test_post_like_recipient_nonexist(self):
        """
        should return 404
        """

        author = self.auth_helper.get_author()
        user = User.objects.create_user("username1")
        author2: Author = Author.objects.get(userId=user)

        post_data = {
            "type":"post",
            "title":"A post title about a post about web dev",
            "description":"This post discusses stuff -- brief",
            "contentType":f"{Post.ContentTypeEnum.MARKDOWN}",
            "author":{
                "type":"author",
                "id":f"{author.id}"
            },
            "visibility":f"{Post.VisibilityEnum.PUBLIC}",
            "unlisted":"false"
        }
        
        response = self.client.post(reverse('post_api:posts', kwargs={'author_id':author.id}), post_data, format="json")
        self.assertEqual(response.status_code, 201, f"expected 201. got: {response.status_code}")
        postId = json.loads(response.content)["data"]["id"]

        data = {
            "object": f"{postId}",
            "author":{
                "type":"author",
                "id":f"{author2.id}"
            },
        }

        authorId = uuid4()
        response = self.client.post(reverse('likes_api:inbox_like', kwargs={'author_id':authorId}), data, format="json")
        self.assertEqual(response.status_code, 404, f"expected 404. got: {response.status_code}")

    def test_post_like_sender_nonexist(self):
        """
        should return 404
        """

        author = self.auth_helper.get_author()

        post_data = {
            "type":"post",
            "title":"A post title about a post about web dev",
            "description":"This post discusses stuff -- brief",
            "contentType":f"{Post.ContentTypeEnum.MARKDOWN}",
            "author":{
                "type":"author",
                "id":f"{author.id}"
            },
            "visibility":f"{Post.VisibilityEnum.PUBLIC}",
            "unlisted":"false"
        }
        
        response = self.client.post(reverse('post_api:posts', kwargs={'author_id':author.id}), post_data, format="json")
        self.assertEqual(response.status_code, 201, f"expected 201. got: {response.status_code}")
        postId = json.loads(response.content)["data"]["id"]

        authorId = uuid4()
        data = {
            "object": f"{postId}",
            "author":{
                "type":"author",
                "id":f"{authorId}"
            },
        }

        response = self.client.post(reverse('likes_api:inbox_like', kwargs={'author_id':author.id}), data, format="json")
        self.assertEqual(response.status_code, 404, f"expected 404. got: {response.status_code}")

    def test_post_like_recipient_bad_uuid(self):
        """
        should return 404
        """

        author = self.auth_helper.get_author()
        user = User.objects.create_user("username1")
        author2: Author = Author.objects.get(userId=user)

        post_data = {
            "type":"post",
            "title":"A post title about a post about web dev",
            "description":"This post discusses stuff -- brief",
            "contentType":f"{Post.ContentTypeEnum.MARKDOWN}",
            "author":{
                "type":"author",
                "id":f"{author.id}"
            },
            "visibility":f"{Post.VisibilityEnum.PUBLIC}",
            "unlisted":"false"
        }
        
        response = self.client.post(reverse('post_api:posts', kwargs={'author_id':author.id}), post_data, format="json")
        self.assertEqual(response.status_code, 201, f"expected 201. got: {response.status_code}")
        postId = json.loads(response.content)["data"]["id"]

        data = {
            "object": f"{postId}",
            "author":{
                "type":"author",
                "id":f"{author2.id}"
            },
        }

        authorId = "notARealUUID"
        response = self.client.post(reverse('likes_api:inbox_like', kwargs={'author_id':authorId}), data, format="json")
        self.assertEqual(response.status_code, 404, f"expected 201. got: {response.status_code}")

    def test_post_like_sender_bad_uuid(self):
        """
        should return 404
        """

        author = self.auth_helper.get_author()

        post_data = {
            "type":"post",
            "title":"A post title about a post about web dev",
            "description":"This post discusses stuff -- brief",
            "contentType":f"{Post.ContentTypeEnum.MARKDOWN}",
            "author":{
                "type":"author",
                "id":f"{author.id}"
            },
            "visibility":f"{Post.VisibilityEnum.PUBLIC}",
            "unlisted":"false"
        }
        
        response = self.client.post(reverse('post_api:posts', kwargs={'author_id':author.id}), post_data, format="json")
        self.assertEqual(response.status_code, 201, f"expected 201. got: {response.status_code}")
        postId = json.loads(response.content)["data"]["id"]

        authorId = "notARealUUID"
        data = {
            "object": f"{postId}",
            "author":{
                "type":"author",
                "id":f"{authorId}"
            },
        }

        response = self.client.post(reverse('likes_api:inbox_like', kwargs={'author_id':author.id}), data, format="json")
        self.assertEqual(response.status_code, 404, f"expected 201. got: {response.status_code}")

    def test_post_like_no_data(self):
        """
        should return 404
        """
        
        author = self.auth_helper.get_author()

        post_data = {
            "type":"post",
            "title":"A post title about a post about web dev",
            "description":"This post discusses stuff -- brief",
            "contentType":f"{Post.ContentTypeEnum.MARKDOWN}",
            "author":{
                "type":"author",
                "id":f"{author.id}"
            },
            "visibility":f"{Post.VisibilityEnum.PUBLIC}",
            "unlisted":"false"
        }
        
        response = self.client.post(reverse('post_api:posts', kwargs={'author_id':author.id}), post_data, format="json")
        self.assertEqual(response.status_code, 201, f"expected 201. got: {response.status_code}")

        data = {}

        response = self.client.post(reverse('likes_api:inbox_like', kwargs={'author_id':author.id}), data, format="json")
        self.assertEqual(response.status_code, 400, f"expected 400. got: {response.status_code}")

    def test_post_like_invalid_object(self):
        """
        should return 404
        """
        
        author = self.auth_helper.get_author()
        user = User.objects.create_user("username1")
        author2: Author = Author.objects.get(userId=user)

        data = {
            "object": f"{uuid4()}",
            "author":{
                "type":"author",
                "id":f"{author2.id}"
            },
        }

        response = self.client.post(reverse('likes_api:inbox_like', kwargs={'author_id':author.id}), data, format="json")
        self.assertEqual(response.status_code, 404, f"expected 404. got: {response.status_code}")

    # GETs #####################

    def test_get_like(self):
        """
        should return inbox items with ids matching the created items
        """
        
        author = self.auth_helper.get_author()
        user = User.objects.create_user("username1")
        author2: Author = Author.objects.get(userId=user)

        post_data = {
            "type":"post",
            "title":"A post title about a post about web dev",
            "description":"This post discusses stuff -- brief",
            "contentType":f"{Post.ContentTypeEnum.MARKDOWN}",
            "author":{
                "type":"author",
                "id":f"{author.id}"
            },
            "visibility":f"{Post.VisibilityEnum.PUBLIC}",
            "unlisted":"false"
        }
        
        response = self.client.post(reverse('post_api:posts', kwargs={'author_id':author.id}), post_data, format="json")

        self.assertEqual(response.status_code, 201, f"expected 201. got: {response.status_code}")
        postId = json.loads(response.content)["data"]["id"]
        postIdFragment = postId.split("posts/")[1].rstrip("/")

        data = {
            "object": f"{postId}",
            "author":{
                "type":"author",
                "id":f"{author2.id}"
            },
        }

        response = self.client.post(reverse('likes_api:inbox_like', kwargs={'author_id':author.id}), data, format="json")
        self.assertEqual(response.status_code, 201, f"expected 201. got: {response.status_code}")
        dict_resp_data = json.loads(response.content)["data"]
        self.assertEqual(postId, dict_resp_data["object"], "returned item referenced wrong object!")
        self.assertEqual(dict_resp_data["author"]["id"], str(author2.id), "returned item referenced wrong author!")
        
        response = self.client.get(reverse('likes_api:post_likes', kwargs={'author_id':author.id, 'post_id':postIdFragment}))
        self.assertEqual(response.status_code, 200, f"expected 200. got: {response.status_code}")
        post_likes = json.loads(response.content)["data"]
        self.assertEqual(len(post_likes), 1, f"expected list of length 1. got: {len(post_likes)}")
        self.assertEqual(postId, post_likes[0]["object"], "returned item referenced wrong object!")
        self.assertEqual(post_likes[0]["author"]["id"], str(author2.id), "returned item referenced wrong author!")

        comment_data = {
            "type":"comment",
            "author":{
                "type":"author",
                "id":f"{author.id}"
            },
            "comment":"A Comment with words and markdown",
            "contentType":f"{Comment.ContentTypeEnum.MARKDOWN}"
        }

        response = self.client.post(reverse('post_api:comments', kwargs={'author_id':author.id, 'post_id':postIdFragment}), comment_data, format="json")
        self.assertEqual(response.status_code, 201, f"expected 201. got: {response.status_code}")

        commentId = json.loads(response.content)["data"]["id"]
        commentIdFragment = commentId.split("comments/")[1].rstrip("/")

        data = {
            "object": f"{commentId}",
            "author":{
                "type":"author",
                "id":f"{author2.id}"
            },
        }

        response = self.client.post(reverse('likes_api:inbox_like', kwargs={'author_id':author.id}), data, format="json")
        self.assertEqual(response.status_code, 201, f"expected 201. got: {response.status_code}")
        dict_resp_data = json.loads(response.content)["data"]
        self.assertEqual(commentId, dict_resp_data["object"], "returned item referenced wrong object!")
        self.assertEqual(dict_resp_data["author"]["id"], str(author2.id), "returned item referenced wrong author!")

        response = self.client.get(reverse('likes_api:comment_likes', kwargs={'author_id':author.id, 'post_id':postIdFragment, 'comment_id':commentIdFragment}))
        self.assertEqual(response.status_code, 200, f"expected 200. got: {response.status_code}")
        comment_likes = json.loads(response.content)["data"]
        self.assertEqual(len(comment_likes), 1, f"expected list of length 1. got: {len(post_likes)}")
        self.assertEqual(commentId, comment_likes[0]["object"], "returned item referenced wrong object!")
        self.assertEqual(comment_likes[0]["author"]["id"], str(author2.id), "returned item referenced wrong author!")

    def test_get_like_access_levels(self):
        """
        should return 200 for all users
        """
        
        password = "password"
        user = User.objects.create_user("username1", password=password)
        author: Author = Author.objects.get(userId=user)
        user2 = User.objects.create_user("username2", password=password)
        author2: Author = Author.objects.get(userId=user2)
        self.client.logout()
        self.client.login(username=user.username, password=password)

        # author creates a post
        post_data = {
            "type":"post",
            "title":"A post title about a post about web dev",
            "description":"This post discusses stuff -- brief",
            "contentType":f"{Post.ContentTypeEnum.MARKDOWN}",
            "author":{
                "type":"author",
                "id":f"{author.id}"
            },
            "visibility":f"{Post.VisibilityEnum.PUBLIC}",
            "unlisted":"false"
        }
        
        response = self.client.post(reverse('post_api:posts', kwargs={'author_id':author.id}), post_data, format="json")

        self.assertEqual(response.status_code, 201, f"expected 201. got: {response.status_code}")
        postId = json.loads(response.content)["data"]["id"]
        postIdFragment = postId.split("posts/")[1].rstrip("/")

        # author2 likes author's post
        self.client.logout()
        self.assertTrue(self.client.login(username=user2.username, password=password))
        data = {
            "object": f"{postId}",
            "author":{
                "type":"author",
                "id":f"{author2.id}"
            },
        }

        response = self.client.post(reverse('likes_api:inbox_like', kwargs={'author_id':author.id}), data, format="json")
        self.assertEqual(response.status_code, 201, f"expected 201. got: {response.status_code}")

        # author comments on their own post
        self.client.logout()
        self.assertTrue(self.client.login(username=user.username, password=password))
        comment_data = {
            "type":"comment",
            "author":{
                "type":"author",
                "id":f"{author.id}"
            },
            "comment":"A Comment with words and markdown",
            "contentType":f"{Comment.ContentTypeEnum.MARKDOWN}"
        }

        response = self.client.post(reverse('post_api:comments', kwargs={'author_id':author.id, 'post_id':postIdFragment}), comment_data, format="json")
        self.assertEqual(response.status_code, 201, f"expected 201. got: {response.status_code}")

        commentId = json.loads(response.content)["data"]["id"]
        commentIdFragment = commentId.split("comments/")[1].rstrip("/")

        # author2 likes author's comment
        self.client.logout()
        self.assertTrue(self.client.login(username=user2.username, password=password))
        data = {
            "object": f"{commentId}",
            "author":{
                "type":"author",
                "id":f"{author2.id}"
            },
        }

        response = self.client.post(reverse('likes_api:inbox_like', kwargs={'author_id':author.id}), data, format="json")
        self.assertEqual(response.status_code, 201, f"expected 201. got: {response.status_code}")

        self.client.logout()
        # test anonymous user
        response = self.client.get(reverse('likes_api:post_likes', kwargs={'author_id':author.id, 'post_id':postIdFragment}))
        self.assertEqual(response.status_code, 200, f"expected 200. got: {response.status_code}")
        response = self.client.get(reverse('likes_api:comment_likes', kwargs={'author_id':author.id, 'post_id':postIdFragment, 'comment_id':commentIdFragment}))
        self.assertEqual(response.status_code, 200, f"expected 200. got: {response.status_code}")
        # test non participant user
        nonParticipant = User.objects.create_user("nonParticipant", password=password)
        self.assertTrue(self.client.login(username=nonParticipant.username, password=password))
        response = self.client.get(reverse('likes_api:post_likes', kwargs={'author_id':author.id, 'post_id':postIdFragment}))
        self.assertEqual(response.status_code, 200, f"expected 200. got: {response.status_code}")
        response = self.client.get(reverse('likes_api:comment_likes', kwargs={'author_id':author.id, 'post_id':postIdFragment, 'comment_id':commentIdFragment}))
        self.assertEqual(response.status_code, 200, f"expected 200. got: {response.status_code}")
        # test likee
        self.client.logout()
        self.assertTrue(self.client.login(username=user.username, password=password))
        response = self.client.get(reverse('likes_api:post_likes', kwargs={'author_id':author.id, 'post_id':postIdFragment}))
        self.assertEqual(response.status_code, 200, f"expected 200. got: {response.status_code}")
        response = self.client.get(reverse('likes_api:comment_likes', kwargs={'author_id':author.id, 'post_id':postIdFragment, 'comment_id':commentIdFragment}))
        self.assertEqual(response.status_code, 200, f"expected 200. got: {response.status_code}")
        # test owner
        self.client.logout()
        self.assertTrue(self.client.login(username=user2.username, password=password))
        response = self.client.get(reverse('likes_api:post_likes', kwargs={'author_id':author.id, 'post_id':postIdFragment}))
        self.assertEqual(response.status_code, 200, f"expected 200. got: {response.status_code}")
        response = self.client.get(reverse('likes_api:comment_likes', kwargs={'author_id':author.id, 'post_id':postIdFragment, 'comment_id':commentIdFragment}))
        self.assertEqual(response.status_code, 200, f"expected 200. got: {response.status_code}")
        # test admin
        self.client.logout()
        self.auth_helper.authorize_client(self.client)
        response = self.client.get(reverse('likes_api:post_likes', kwargs={'author_id':author.id, 'post_id':postIdFragment}))
        self.assertEqual(response.status_code, 200, f"expected 200. got: {response.status_code}")
        response = self.client.get(reverse('likes_api:comment_likes', kwargs={'author_id':author.id, 'post_id':postIdFragment, 'comment_id':commentIdFragment}))
        self.assertEqual(response.status_code, 200, f"expected 200. got: {response.status_code}")
        
    def test_get_like_nonexist(self):
        """
        should return 404
        """
        
        author = self.auth_helper.get_author()
        postIdFragment = uuid4()

        response = self.client.get(reverse('likes_api:post_likes', kwargs={'author_id':author.id, 'post_id':postIdFragment}))
        self.assertEqual(response.status_code, 404, f"expected 404. got: {response.status_code}")

        # actually make a post now so we can soley test getting a comment that doesn't exist
        user = User.objects.create_user("username1")
        author2: Author = Author.objects.get(userId=user)

        post_data = {
            "type":"post",
            "title":"A post title about a post about web dev",
            "description":"This post discusses stuff -- brief",
            "contentType":f"{Post.ContentTypeEnum.MARKDOWN}",
            "author":{
                "type":"author",
                "id":f"{author.id}"
            },
            "visibility":f"{Post.VisibilityEnum.PUBLIC}",
            "unlisted":"false"
        }
        
        response = self.client.post(reverse('post_api:posts', kwargs={'author_id':author.id}), post_data, format="json")
        self.assertEqual(response.status_code, 201, f"expected 201. got: {response.status_code}")
        postId = json.loads(response.content)["data"]["id"]
        postIdFragment = postId.split("posts/")[1].rstrip("/")

        data = {
            "object": f"{postId}",
            "author":{
                "type":"author",
                "id":f"{author2.id}"
            },
        }

        response = self.client.post(reverse('likes_api:inbox_like', kwargs={'author_id':author.id}), data, format="json")
        self.assertEqual(response.status_code, 201, f"expected 201. got: {response.status_code}")
        dict_resp_data = json.loads(response.content)["data"]
        self.assertEqual(postId, dict_resp_data["object"], "returned item referenced wrong object!")
        self.assertEqual(dict_resp_data["author"]["id"], str(author2.id), "returned item referenced wrong author!")

        commentIdFragment = uuid4()
        response = self.client.get(reverse('likes_api:comment_likes', kwargs={'author_id':author.id, 'post_id':postIdFragment, 'comment_id':commentIdFragment}))
        self.assertEqual(response.status_code, 404, f"expected 404. got: {response.status_code}")

    def test_get_like_bad_uuid(self):
        """
        should return 404
        """
        
        author = self.auth_helper.get_author()
        postIdFragment = "notARealUUID"

        response = self.client.get(reverse('likes_api:post_likes', kwargs={'author_id':author.id, 'post_id':postIdFragment}))
        self.assertEqual(response.status_code, 404, f"expected 404. got: {response.status_code}")


        # actually make a post now so we can soley test getting a comment that doesn't exist
        user = User.objects.create_user("username1")
        author2: Author = Author.objects.get(userId=user)

        post_data = {
            "type":"post",
            "title":"A post title about a post about web dev",
            "description":"This post discusses stuff -- brief",
            "contentType":f"{Post.ContentTypeEnum.MARKDOWN}",
            "author":{
                "type":"author",
                "id":f"{author.id}"
            },
            "visibility":f"{Post.VisibilityEnum.PUBLIC}",
            "unlisted":"false"
        }
        
        response = self.client.post(reverse('post_api:posts', kwargs={'author_id':author.id}), post_data, format="json")
        self.assertEqual(response.status_code, 201, f"expected 201. got: {response.status_code}")
        postId = json.loads(response.content)["data"]["id"]
        postIdFragment = postId.split("posts/")[1].rstrip("/")

        data = {
            "object": f"{postId}",
            "author":{
                "type":"author",
                "id":f"{author2.id}"
            },
        }

        response = self.client.post(reverse('likes_api:inbox_like', kwargs={'author_id':author.id}), data, format="json")
        self.assertEqual(response.status_code, 201, f"expected 201. got: {response.status_code}")
        dict_resp_data = json.loads(response.content)["data"]
        self.assertEqual(postId, dict_resp_data["object"], "returned item referenced wrong object!")
        self.assertEqual(dict_resp_data["author"]["id"], str(author2.id), "returned item referenced wrong author!")

        commentIdFragment = "notARealUUID"
        response = self.client.get(reverse('likes_api:comment_likes', kwargs={'author_id':author.id, 'post_id':postIdFragment, 'comment_id':commentIdFragment}))
        self.assertEqual(response.status_code, 404, f"expected 404. got: {response.status_code}")

    def test_get_like_recipient_nonexist(self):
        """
        should return 404
        """
        
        author = self.auth_helper.get_author()
        user = User.objects.create_user("username1")
        author2: Author = Author.objects.get(userId=user)

        post_data = {
            "type":"post",
            "title":"A post title about a post about web dev",
            "description":"This post discusses stuff -- brief",
            "contentType":f"{Post.ContentTypeEnum.MARKDOWN}",
            "author":{
                "type":"author",
                "id":f"{author.id}"
            },
            "visibility":f"{Post.VisibilityEnum.PUBLIC}",
            "unlisted":"false"
        }
        
        response = self.client.post(reverse('post_api:posts', kwargs={'author_id':author.id}), post_data, format="json")
        self.assertEqual(response.status_code, 201, f"expected 201. got: {response.status_code}")
        postId = json.loads(response.content)["data"]["id"]
        postIdFragment = postId.split("posts/")[1].rstrip("/")

        data = {
            "object": f"{postId}",
            "author":{
                "type":"author",
                "id":f"{author2.id}"
            },
        }

        response = self.client.post(reverse('likes_api:inbox_like', kwargs={'author_id':author.id}), data, format="json")
        self.assertEqual(response.status_code, 201, f"expected 201. got: {response.status_code}")
        dict_resp_data = json.loads(response.content)["data"]
        self.assertEqual(postId, dict_resp_data["object"], "returned item referenced wrong object!")
        self.assertEqual(dict_resp_data["author"]["id"], str(author2.id), "returned item referenced wrong author!")

        authorId = uuid4()
        response = self.client.get(reverse('likes_api:post_likes', kwargs={'author_id':authorId, 'post_id':postIdFragment}))
        self.assertEqual(response.status_code, 404, f"expected 404. got: {response.status_code}")

    def test_get_like_recipient_bad_uuid(self):
        """
        should return 404
        """
        
        author = self.auth_helper.get_author()
        user = User.objects.create_user("username1")
        author2: Author = Author.objects.get(userId=user)

        post_data = {
            "type":"post",
            "title":"A post title about a post about web dev",
            "description":"This post discusses stuff -- brief",
            "contentType":f"{Post.ContentTypeEnum.MARKDOWN}",
            "author":{
                "type":"author",
                "id":f"{author.id}"
            },
            "visibility":f"{Post.VisibilityEnum.PUBLIC}",
            "unlisted":"false"
        }
        
        response = self.client.post(reverse('post_api:posts', kwargs={'author_id':author.id}), post_data, format="json")
        self.assertEqual(response.status_code, 201, f"expected 201. got: {response.status_code}")
        postId = json.loads(response.content)["data"]["id"]
        postIdFragment = postId.split("posts/")[1].rstrip("/")

        data = {
            "object": f"{postId}",
            "author":{
                "type":"author",
                "id":f"{author2.id}"
            },
        }

        response = self.client.post(reverse('likes_api:inbox_like', kwargs={'author_id':author.id}), data, format="json")
        self.assertEqual(response.status_code, 201, f"expected 201. got: {response.status_code}")
        dict_resp_data = json.loads(response.content)["data"]
        self.assertEqual(postId, dict_resp_data["object"], "returned item referenced wrong object!")
        self.assertEqual(dict_resp_data["author"]["id"], str(author2.id), "returned item referenced wrong author!")

        authorId = "notARealUUID"
        response = self.client.get(reverse('likes_api:post_likes', kwargs={'author_id':authorId, 'post_id':postIdFragment}))
        self.assertEqual(response.status_code, 404, f"expected 404. got: {response.status_code}")

    def test_get_liked_things(self):
        """
        should return inbox items with ids matching the created items
        """
        
        author = self.auth_helper.get_author()
        user = User.objects.create_user("username1")
        author2: Author = Author.objects.get(userId=user)

        post_data = {
            "type":"post",
            "title":"A post title about a post about web dev",
            "description":"This post discusses stuff -- brief",
            "contentType":f"{Post.ContentTypeEnum.MARKDOWN}",
            "author":{
                "type":"author",
                "id":f"{author.id}"
            },
            "visibility":f"{Post.VisibilityEnum.PUBLIC}",
            "unlisted":"false"
        }
        
        response = self.client.post(reverse('post_api:posts', kwargs={'author_id':author.id}), post_data, format="json")
        self.assertEqual(response.status_code, 201, f"expected 201. got: {response.status_code}")
        postId = json.loads(response.content)["data"]["id"]
        postIdFragment = postId.split("posts/")[1].rstrip("/")

        data = {
            "object": f"{postId}",
            "author":{
                "type":"author",
                "id":f"{author2.id}"
            },
        }

        response = self.client.post(reverse('likes_api:inbox_like', kwargs={'author_id':author.id}), data, format="json")
        self.assertEqual(response.status_code, 201, f"expected 201. got: {response.status_code}")
        dict_resp_data = json.loads(response.content)["data"]
        self.assertEqual(postId, dict_resp_data["object"], "returned item referenced wrong object!")
        self.assertEqual(dict_resp_data["author"]["id"], str(author2.id), "returned item referenced wrong author!")

        comment_data = {
            "type":"comment",
            "author":{
                "type":"author",
                "id":f"{author.id}"
            },
            "comment":"A Comment with words and markdown",
            "contentType":f"{Comment.ContentTypeEnum.MARKDOWN}"
        }

        response = self.client.post(reverse('post_api:comments', kwargs={'author_id':author.id, 'post_id':postIdFragment}), comment_data, format="json")
        self.assertEqual(response.status_code, 201, f"expected 201. got: {response.status_code}")

        commentId = json.loads(response.content)["data"]["id"]

        data = {
            "object": f"{commentId}",
            "author":{
                "type":"author",
                "id":f"{author2.id}"
            },
        }

        response = self.client.post(reverse('likes_api:inbox_like', kwargs={'author_id':author.id}), data, format="json")
        self.assertEqual(response.status_code, 201, f"expected 201. got: {response.status_code}")
        dict_resp_data = json.loads(response.content)["data"]
        self.assertEqual(commentId, dict_resp_data["object"], "returned item referenced wrong object!")
        self.assertEqual(dict_resp_data["author"]["id"], str(author2.id), "returned item referenced wrong author!")

        response = self.client.get(reverse('likes_api:liked', kwargs={'author_id':author2.id}))
        self.assertEqual(response.status_code, 200, f"expected 200. got: {response.status_code}")
        likes = json.loads(response.content)["data"]
        self.assertEqual(len(likes), 2, f"expected list of length 2. got: {len(likes)}")

        data1 = likes[0]
        data2 = likes[1]
        if data1["object"] == commentId:
            temp = data1
            data1 = data2
            data2 = temp
        self.assertEqual(postId, data1["object"], "returned item referenced wrong object!")
        self.assertEqual(data1["author"]["id"], str(author2.id), "returned item referenced wrong author!")

        self.assertEqual(commentId, data2["object"], "returned item referenced wrong object!")
        self.assertEqual(data2["author"]["id"], str(author2.id), "returned item referenced wrong author!")

    def test_get_liked_things_empty(self):
        """
        should return an empty list
        """
        
        author = self.auth_helper.get_author()

        response = self.client.get(reverse('likes_api:liked', kwargs={'author_id':author.id}))
        self.assertEqual(response.status_code, 200, f"expected 200. got: {response.status_code}")
        likes = json.loads(response.content)["data"]
        self.assertEqual(len(likes), 0, "list should have been empty but wasn't!")

    def test_get_liked_things_sender_nonexist(self):
        """
        should return an empty list
        """
        
        authorId = uuid4()

        response = self.client.get(reverse('likes_api:liked', kwargs={'author_id':authorId}))
        self.assertEqual(response.status_code, 200, f"expected 200. got: {response.status_code}")
        likes = json.loads(response.content)["data"]
        self.assertEqual(len(likes), 0, "list should have been empty but wasn't!")

    def test_get_liked_things_sender_bad_uuid(self):
        """
        should return an empty list
        """
        
        authorId = "notARealUUID"

        response = self.client.get(reverse('likes_api:liked', kwargs={'author_id':authorId}))
        self.assertEqual(response.status_code, 200, f"expected 200. got: {response.status_code}")
        likes = json.loads(response.content)["data"]
        self.assertEqual(len(likes), 0, "list should have been empty but wasn't!")
