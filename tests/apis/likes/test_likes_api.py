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
        user = User(username="username1")
        user.save()
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
        user = User(username="username1")
        user.save()
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
        user = User(username="username1")
        user.save()
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
        user = User(username="username1")
        user.save()
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
        user = User(username="username1")
        user.save()
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

    def test_get_like_nonexist(self):
        """
        should return 404
        """
        
        author = self.auth_helper.get_author()
        postIdFragment = uuid4()

        response = self.client.get(reverse('likes_api:post_likes', kwargs={'author_id':author.id, 'post_id':postIdFragment}))
        self.assertEqual(response.status_code, 404, f"expected 404. got: {response.status_code}")

        # actually make a post now so we can soley test getting a comment that doesn't exist
        user = User(username="username1")
        user.save()
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
        user = User(username="username1")
        user.save()
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
        user = User(username="username1")
        user.save()
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
        user = User(username="username1")
        user.save()
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
        user = User(username="username1")
        user.save()
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
