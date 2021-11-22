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
        self.assertEqual(response.status_code, 201)
        postId = json.loads(response.content)["data"]["id"]
        postIdFragment = postId.split("posts/")[1].rstrip("/")

        data = {
            "object": f"{postIdFragment}",
            "author":{
                "type":"author",
                "id":f"{author2.id}"
            },
        }

        response = self.client.post(reverse('likes_api:inbox_like', kwargs={'author_id':author.id}), data, format="json")
        self.assertEqual(response.status_code, 201)
        dict_resp_data = json.loads(response.content)["data"]
        # print("post: " + postId)
        # print("api: " + dict_resp_data["object"])
        # TODO: fix uncomment after we standardize ids
        # self.assertEqual(postId, dict_resp_data["object"])
        self.assertEqual(dict_resp_data["author"]["id"], str(author2.id))

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
        self.assertEqual(response.status_code, 201)

        commentId = json.loads(response.content)["data"]["id"]
        commentIdFragment = commentId.split("comments/")[1].rstrip("/")

        data = {
            "object": f"{commentIdFragment}",
            "author":{
                "type":"author",
                "id":f"{author2.id}"
            },
        }

        response = self.client.post(reverse('likes_api:inbox_like', kwargs={'author_id':author.id}), data, format="json")
        self.assertEqual(response.status_code, 201)
        dict_resp_data = json.loads(response.content)["data"]
        # print("post: " + postId)
        # print("api: " + dict_resp_data["object"])
        # TODO: fix uncomment after we standardize ids
        # self.assertEqual(commentId, dict_resp_data["object"])
        self.assertEqual(dict_resp_data["author"]["id"], str(author2.id))

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
        self.assertEqual(response.status_code, 201)
        postId = json.loads(response.content)["data"]["id"]
        postIdFragment = postId.split("posts/")[1].rstrip("/")

        data = {
            "object": f"{postIdFragment}",
            "author":{
                "type":"author",
                "id":f"{author.id}"
            },
        }

        response = self.client.post(reverse('likes_api:inbox_like', kwargs={'author_id':author.id}), data, format="json")
        self.assertEqual(response.status_code, 201)
        dict_resp_data = json.loads(response.content)["data"]
        # print("post: " + postId)
        # print("api: " + dict_resp_data["object"])
        # TODO: fix uncomment after we standardize ids
        # self.assertEqual(postId, dict_resp_data["object"])
        self.assertEqual(dict_resp_data["author"]["id"], str(author.id))

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
        self.assertEqual(response.status_code, 201)

        commentId = json.loads(response.content)["data"]["id"]
        commentIdFragment = commentId.split("comments/")[1].rstrip("/")

        data = {
            "object": f"{commentIdFragment}",
            "author":{
                "type":"author",
                "id":f"{author.id}"
            },
        }

        response = self.client.post(reverse('likes_api:inbox_like', kwargs={'author_id':author.id}), data, format="json")
        self.assertEqual(response.status_code, 201)
        dict_resp_data = json.loads(response.content)["data"]
        # print("post: " + postId)
        # print("api: " + dict_resp_data["object"])
        # TODO: fix uncomment after we standardize ids
        # self.assertEqual(commentId, dict_resp_data["object"])
        self.assertEqual(dict_resp_data["author"]["id"], str(author.id))

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
        self.assertEqual(response.status_code, 201)
        postId = json.loads(response.content)["data"]["id"]
        postIdFragment = postId.split("posts/")[1].rstrip("/")

        data = {
            "object": f"{postIdFragment}",
            "author":{
                "type":"author",
                "id":f"{author2.id}"
            },
        }

        authorId = uuid4()
        response = self.client.post(reverse('likes_api:inbox_like', kwargs={'author_id':authorId}), data, format="json")
        self.assertEqual(response.status_code, 404)

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
        self.assertEqual(response.status_code, 201)
        postId = json.loads(response.content)["data"]["id"]
        postIdFragment = postId.split("posts/")[1].rstrip("/")

        authorId = uuid4()
        data = {
            "object": f"{postIdFragment}",
            "author":{
                "type":"author",
                "id":f"{authorId}"
            },
        }

        response = self.client.post(reverse('likes_api:inbox_like', kwargs={'author_id':author.id}), data, format="json")
        self.assertEqual(response.status_code, 404)

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
        self.assertEqual(response.status_code, 201)
        postId = json.loads(response.content)["data"]["id"]
        postIdFragment = postId.split("posts/")[1].rstrip("/")

        data = {
            "object": f"{postIdFragment}",
            "author":{
                "type":"author",
                "id":f"{author2.id}"
            },
        }

        authorId = "notARealUUID"
        response = self.client.post(reverse('likes_api:inbox_like', kwargs={'author_id':authorId}), data, format="json")
        self.assertEqual(response.status_code, 404)

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
        self.assertEqual(response.status_code, 201)
        postId = json.loads(response.content)["data"]["id"]
        postIdFragment = postId.split("posts/")[1].rstrip("/")

        authorId = "notARealUUID"
        data = {
            "object": f"{postIdFragment}",
            "author":{
                "type":"author",
                "id":f"{authorId}"
            },
        }

        response = self.client.post(reverse('likes_api:inbox_like', kwargs={'author_id':author.id}), data, format="json")
        self.assertEqual(response.status_code, 404)

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
        self.assertEqual(response.status_code, 201)

        data = {}

        response = self.client.post(reverse('likes_api:inbox_like', kwargs={'author_id':author.id}), data, format="json")
        self.assertEqual(response.status_code, 404)

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
        self.assertEqual(response.status_code, 404)

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
        self.assertEqual(response.status_code, 201)
        postId = json.loads(response.content)["data"]["id"]
        postIdFragment = postId.split("posts/")[1].rstrip("/")

        data = {
            "object": f"{postIdFragment}",
            "author":{
                "type":"author",
                "id":f"{author2.id}"
            },
        }

        response = self.client.post(reverse('likes_api:inbox_like', kwargs={'author_id':author.id}), data, format="json")
        self.assertEqual(response.status_code, 201)
        dict_resp_data = json.loads(response.content)["data"]
        # print("post: " + postId)
        # print("api: " + dict_resp_data["object"])
        # TODO: fix uncomment after we standardize ids
        # self.assertEqual(postId, dict_resp_data["object"])
        self.assertEqual(dict_resp_data["author"]["id"], str(author2.id))

        response = self.client.get(reverse('likes_api:post_likes', kwargs={'author_id':author.id, 'post_id':postIdFragment}))
        self.assertEqual(response.status_code, 200)
        post_likes = json.loads(response.content)["items"]
        self.assertEqual(len(post_likes), 1)
        # self.assertEqual(postId, post_likes[0]["object"])
        self.assertEqual(post_likes[0]["author"]["id"], str(author2.id))

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
        self.assertEqual(response.status_code, 201)

        commentId = json.loads(response.content)["data"]["id"]
        commentIdFragment = commentId.split("comments/")[1].rstrip("/")

        data = {
            "object": f"{commentIdFragment}",
            "author":{
                "type":"author",
                "id":f"{author2.id}"
            },
        }

        response = self.client.post(reverse('likes_api:inbox_like', kwargs={'author_id':author.id}), data, format="json")
        self.assertEqual(response.status_code, 201)
        dict_resp_data = json.loads(response.content)["data"]
        # print("comment: " + commentId)
        # print("api: " + dict_resp_data["object"])
        # TODO: fix uncomment after we standardize ids
        # self.assertEqual(commentId, dict_resp_data["object"])
        self.assertEqual(dict_resp_data["author"]["id"], str(author2.id))

        response = self.client.get(reverse('likes_api:comment_likes', kwargs={'author_id':author.id, 'post_id':postIdFragment, 'comment_id':commentIdFragment}))
        self.assertEqual(response.status_code, 200)
        comment_likes = json.loads(response.content)["items"]
        self.assertEqual(len(comment_likes), 1)
        # self.assertEqual(commentId, comment_likes[0]["object"])
        self.assertEqual(comment_likes[0]["author"]["id"], str(author2.id))

    def test_get_like_nonexist(self):
        """
        should return inbox items with ids matching the created items
        """
        
        author = self.auth_helper.get_author()
        postIdFragment = uuid4()

        response = self.client.get(reverse('likes_api:post_likes', kwargs={'author_id':author.id, 'post_id':postIdFragment}))
        self.assertEqual(response.status_code, 404)


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
        self.assertEqual(response.status_code, 201)
        postId = json.loads(response.content)["data"]["id"]
        postIdFragment = postId.split("posts/")[1].rstrip("/")

        data = {
            "object": f"{postIdFragment}",
            "author":{
                "type":"author",
                "id":f"{author2.id}"
            },
        }

        response = self.client.post(reverse('likes_api:inbox_like', kwargs={'author_id':author.id}), data, format="json")
        self.assertEqual(response.status_code, 201)
        dict_resp_data = json.loads(response.content)["data"]
        # print("post: " + postId)
        # print("api: " + dict_resp_data["object"])
        # TODO: fix uncomment after we standardize ids
        # self.assertEqual(postId, dict_resp_data["object"])
        self.assertEqual(dict_resp_data["author"]["id"], str(author2.id))

        commentIdFragment = uuid4()
        response = self.client.get(reverse('likes_api:comment_likes', kwargs={'author_id':author.id, 'post_id':postIdFragment, 'comment_id':commentIdFragment}))
        self.assertEqual(response.status_code, 404)

    def test_get_like_bad_uuid(self):
        """
        should return inbox items with ids matching the created items
        """
        
        author = self.auth_helper.get_author()
        postIdFragment = "notARealUUID"

        response = self.client.get(reverse('likes_api:post_likes', kwargs={'author_id':author.id, 'post_id':postIdFragment}))
        self.assertEqual(response.status_code, 404)


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
        self.assertEqual(response.status_code, 201)
        postId = json.loads(response.content)["data"]["id"]
        postIdFragment = postId.split("posts/")[1].rstrip("/")

        data = {
            "object": f"{postIdFragment}",
            "author":{
                "type":"author",
                "id":f"{author2.id}"
            },
        }

        response = self.client.post(reverse('likes_api:inbox_like', kwargs={'author_id':author.id}), data, format="json")
        self.assertEqual(response.status_code, 201)
        dict_resp_data = json.loads(response.content)["data"]
        # print("post: " + postId)
        # print("api: " + dict_resp_data["object"])
        # TODO: fix uncomment after we standardize ids
        # self.assertEqual(postId, dict_resp_data["object"])
        self.assertEqual(dict_resp_data["author"]["id"], str(author2.id))

        commentIdFragment = "notARealUUID"
        response = self.client.get(reverse('likes_api:comment_likes', kwargs={'author_id':author.id, 'post_id':postIdFragment, 'comment_id':commentIdFragment}))
        self.assertEqual(response.status_code, 404)

    def test_get_like_recipient_nonexist(self):
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
        self.assertEqual(response.status_code, 201)
        postId = json.loads(response.content)["data"]["id"]
        postIdFragment = postId.split("posts/")[1].rstrip("/")

        data = {
            "object": f"{postIdFragment}",
            "author":{
                "type":"author",
                "id":f"{author2.id}"
            },
        }

        response = self.client.post(reverse('likes_api:inbox_like', kwargs={'author_id':author.id}), data, format="json")
        self.assertEqual(response.status_code, 201)
        dict_resp_data = json.loads(response.content)["data"]
        # print("post: " + postId)
        # print("api: " + dict_resp_data["object"])
        # TODO: fix uncomment after we standardize ids
        # self.assertEqual(postId, dict_resp_data["object"])
        self.assertEqual(dict_resp_data["author"]["id"], str(author2.id))

        authorId = uuid4()
        response = self.client.get(reverse('likes_api:post_likes', kwargs={'author_id':authorId, 'post_id':postIdFragment}))
        self.assertEqual(response.status_code, 404)

    def test_get_like_recipient_bad_uuid(self):
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
        self.assertEqual(response.status_code, 201)
        postId = json.loads(response.content)["data"]["id"]
        postIdFragment = postId.split("posts/")[1].rstrip("/")

        data = {
            "object": f"{postIdFragment}",
            "author":{
                "type":"author",
                "id":f"{author2.id}"
            },
        }

        response = self.client.post(reverse('likes_api:inbox_like', kwargs={'author_id':author.id}), data, format="json")
        self.assertEqual(response.status_code, 201)
        dict_resp_data = json.loads(response.content)["data"]
        # print("post: " + postId)
        # print("api: " + dict_resp_data["object"])
        # TODO: fix uncomment after we standardize ids
        # self.assertEqual(postId, dict_resp_data["object"])
        self.assertEqual(dict_resp_data["author"]["id"], str(author2.id))

        authorId = "notARealUUID"
        response = self.client.get(reverse('likes_api:post_likes', kwargs={'author_id':authorId, 'post_id':postIdFragment}))
        self.assertEqual(response.status_code, 404)

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
        self.assertEqual(response.status_code, 201)
        postId = json.loads(response.content)["data"]["id"]
        postIdFragment = postId.split("posts/")[1].rstrip("/")

        data = {
            "object": f"{postIdFragment}",
            "author":{
                "type":"author",
                "id":f"{author2.id}"
            },
        }

        response = self.client.post(reverse('likes_api:inbox_like', kwargs={'author_id':author.id}), data, format="json")
        self.assertEqual(response.status_code, 201)
        dict_resp_data = json.loads(response.content)["data"]
        # print("post: " + postId)
        # print("api: " + dict_resp_data["object"])
        # TODO: fix uncomment after we standardize ids
        # self.assertEqual(postId, dict_resp_data["object"])
        self.assertEqual(dict_resp_data["author"]["id"], str(author2.id))

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
        self.assertEqual(response.status_code, 201)

        commentId = json.loads(response.content)["data"]["id"]
        commentIdFragment = commentId.split("comments/")[1].rstrip("/")

        data = {
            "object": f"{commentIdFragment}",
            "author":{
                "type":"author",
                "id":f"{author2.id}"
            },
        }

        response = self.client.post(reverse('likes_api:inbox_like', kwargs={'author_id':author.id}), data, format="json")
        self.assertEqual(response.status_code, 201)
        dict_resp_data = json.loads(response.content)["data"]
        # print("comment: " + commentId)
        # print("api: " + dict_resp_data["object"])
        # TODO: uncomment after we standardize ids
        # self.assertEqual(commentId, dict_resp_data["object"])
        self.assertEqual(dict_resp_data["author"]["id"], str(author2.id))

        response = self.client.get(reverse('likes_api:liked', kwargs={'author_id':author2.id}))
        self.assertEqual(response.status_code, 200)
        likes = json.loads(response.content)["items"]
        self.assertEqual(len(likes), 2)

        # TODO; complete after after we standardize ids
        # data1 = likes[0]
        # data2 = likes[1]
        # # self.assertEqual(postId, data1["object"])
        # self.assertEqual(data1["author"]["id"], str(author2.id))


        # # self.assertEqual(commentId, data2["object"])
        # self.assertEqual(data2["author"]["id"], str(author2.id))

    def test_get_liked_things_empty(self):
        """
        should return an empty list
        """
        
        author = self.auth_helper.get_author()

        response = self.client.get(reverse('likes_api:liked', kwargs={'author_id':author.id}))
        self.assertEqual(response.status_code, 200)
        likes = json.loads(response.content)["items"]
        self.assertEqual(len(likes), 0)

    def test_get_liked_things_sender_nonexist(self):
        """
        should return an empty list
        """
        
        authorId = uuid4()

        response = self.client.get(reverse('likes_api:liked', kwargs={'author_id':authorId}))
        self.assertEqual(response.status_code, 200)
        likes = json.loads(response.content)["items"]
        self.assertEqual(len(likes), 0)

    def test_get_liked_things_sender_bad_uuid(self):
        """
        should return 404
        """
        
        authorId = "notARealUUID"

        response = self.client.get(reverse('likes_api:liked', kwargs={'author_id':authorId}))
        self.assertEqual(response.status_code, 404)