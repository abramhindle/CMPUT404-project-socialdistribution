from django.test import TestCase
from django.urls import reverse
import json

from rest_framework.test import APIClient

from tests.test_helper.auth_helper import AuthHelper

from socialdistribution.pagination import DEFAULT_PAGE
from socialdistribution.pagination import DEFAULT_PAGE_SIZE

from apps.core.models import Author, User
from apps.posts.models import Post, Comment

from uuid import uuid4

class PostsViewTests(TestCase):

    def setUp(self):
        self.auth_helper = AuthHelper()
        self.auth_helper.setup()
        self.client = APIClient()
        self.auth_helper.authorize_client(self.client)

    # ############################################################
    # # TESTS FOR the view class "posts"
    # ############################################################

    def test_get_posts_empty(self):
        """
        should return 200 with no data except pagination
        """
        
        author = self.auth_helper.get_author()
        response = self.client.get(reverse('post_api:posts', kwargs={'author_id':author.id}))

        self.assertEqual(response.status_code, 200)
        dict_resp = json.loads(response.content)

        # checking default pagination
        self.assertEqual(dict_resp["page"], DEFAULT_PAGE)
        self.assertEqual(dict_resp["size"], DEFAULT_PAGE_SIZE)

        self.assertEqual(len(dict_resp["data"]), 0)

    def test_get_posts(self):
        """
        should return all posts
        """
        
        author = self.auth_helper.get_author()

        post1 = {
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

        post2 = {
            "type":"post",
            "title":"A post title about a post about web dev 2",
            "description":"This post discusses stuff -- brief 2",
            "contentType":f"{Post.ContentTypeEnum.PLAIN}",
            "author":{
                "type":"author",
                "id":f"{author.id}"
            },
            "visibility":f"{Post.VisibilityEnum.FRIENDS}",
            "unlisted":"false"
        }

        response = self.client.post(reverse('post_api:posts', kwargs={'author_id':author.id}), post1, format="json")
        self.assertEqual(response.status_code, 201)
        response = self.client.post(reverse('post_api:posts', kwargs={'author_id':author.id}), post2, format="json")
        self.assertEqual(response.status_code, 201)
        response = self.client.get(reverse('post_api:posts', kwargs={'author_id':author.id}))
        self.assertEqual(response.status_code, 200)
        dict_resp = json.loads(response.content)
        dict_resp_data = dict_resp["data"]

        # checking default pagination
        self.assertEqual(dict_resp["page"], DEFAULT_PAGE)
        self.assertEqual(dict_resp["size"], DEFAULT_PAGE_SIZE)

        self.assertEqual(len(dict_resp_data), 2, f"expected 2 posts. got: {len(dict_resp_data)}")

        data1 = dict_resp_data[0]
        data2 = dict_resp_data[1]

        if(data1["title"] != post1["title"]):
            temp = data2
            data2 = data1
            data1 = temp

        # print(dict_resp_data)

        self.assertEqual(data1["type"], post1["type"])
        self.assertEqual(data1["title"], post1["title"])
        self.assertEqual(data1["description"], post1["description"])
        self.assertEqual(data1["contentType"], post1["contentType"])
        self.assertEqual(data1["visibility"], post1["visibility"])
        # Public post uri-id contains its authors id in it
        self.assertIn(str(author.id), data1["id"])

        self.assertEqual(data2["type"], post2["type"])
        self.assertEqual(data2["title"], post2["title"])
        self.assertEqual(data2["description"], post2["description"])
        self.assertEqual(data2["contentType"], post2["contentType"])
        self.assertEqual(data2["visibility"], post2["visibility"])
        # Public post uri-id contains its authors id in it
        self.assertIn(str(author.id), data2["id"])

    def test_get_posts_bad_uuid(self):
        """
        should return 404
        """

        response = self.client.get(reverse('post_api:posts', kwargs={'author_id':'notARealUUID'}))
        self.assertEqual(response.status_code, 404)

    def test_get_posts_author_nonexist(self):
        """
        should return 404
        """

        response = self.client.get(reverse('post_api:posts', kwargs={'author_id': '0b552c30-0a2e-445e-828d-b356b5276c0f'}))
        self.assertEqual(response.status_code, 404)

    # def test_get_posts_multiple_authors(self):
    #     """
    #     should only return posts from the correct author
    #     """
        
    #     author = self.auth_helper.get_author()
    #     user2 = User.objects.create_superuser("username", "email@email.com", "password")
    #     author2 = Author.objects.get(userId=user2.id)
    #     client2 = APIClient()
    #     client2.login(username="username", password="password")
    #     # author2: Author = Author.objects.get(userId=user2.id)
    #     # self.client.login(username="username", password="pwd")    

    #     post1 = {
    #         "type":"post",
    #         "title":"A post title about a post about web dev",
    #         "description":"This post discusses stuff -- brief",
    #         "contentType":f"{Post.ContentTypeEnum.MARKDOWN}",
    #         "author":{
    #             "type":"author",
    #             "id":f"{author.id}"
    #         },
    #         "visibility":f"{Post.VisibilityEnum.PUBLIC}",
    #         "unlisted":"false"
    #     }

    #     post2 = {
    #         "type":"post",
    #         "title":"A post title about a post about web dev 2",
    #         "description":"This post discusses stuff -- brief 2",
    #         "contentType":f"{Post.ContentTypeEnum.PLAIN}",
    #         "author":{
    #             "type":"author",
    #             "id":f"{author2.id}"
    #         },
    #         "visibility":f"{Post.VisibilityEnum.FRIENDS}",
    #         "unlisted":"false"
    #     }

    #     response = self.client.post(reverse('post_api:posts', kwargs={'author_id':author.id}), post1, format="json")
    #     self.assertEqual(response.status_code, 201)
    #     response = self.client.post(reverse('post_api:posts', kwargs={'author_id':author2.id}), post2, format="json")
    #     self.assertEqual(response.status_code, 201)
    #     response = self.client.get(reverse('post_api:posts', kwargs={'author_id':author.id}))
    #     self.assertEqual(response.status_code, 200)
    #     dict_resp = json.loads(response.content)
    #     dict_resp_data = dict_resp["data"][0]

    #     # checking default pagination
    #     self.assertEqual(dict_resp["page"], DEFAULT_PAGE)
    #     self.assertEqual(dict_resp["size"], DEFAULT_PAGE_SIZE)
    #     # print(dict_resp_data)

    #     self.assertEqual(dict_resp_data["type"], post1["type"])
    #     self.assertEqual(dict_resp_data["title"], post1["title"])
    #     self.assertEqual(dict_resp_data["description"], post1["description"])
    #     self.assertEqual(dict_resp_data["contentType"], post1["contentType"])
    #     self.assertEqual(dict_resp_data["visibility"], post1["visibility"])
    #     # Public post uri-id contains its authors id in it
    #     self.assertIn(str(author.id), dict_resp_data["id"])

    def test_post_post(self):
        """
        should return the created post
        """

        author = self.auth_helper.get_author()

        data = {
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
        
        response = self.client.post(reverse('post_api:posts', kwargs={'author_id':author.id}), data, format="json")
        self.assertEqual(response.status_code, 201)
    
        dict_resp = json.loads(response.content)
        dict_resp_data = dict_resp["data"]
        self.assertEqual(dict_resp_data["type"], data["type"])
        self.assertEqual(dict_resp_data["title"], data["title"])
        self.assertEqual(dict_resp_data["description"], data["description"])
        self.assertEqual(dict_resp_data["contentType"], data["contentType"])
        self.assertEqual(dict_resp_data["visibility"], data["visibility"])
        # Public post uri-id contains its authors id in it
        self.assertIn(str(author.id), dict_resp_data["id"])

    def test_post_post_no_data(self):
        """
        should return the created post
        """

        author = self.auth_helper.get_author()

        data = {}
        
        response = self.client.post(reverse('post_api:posts', kwargs={'author_id':author.id}), data, format="json")
        self.assertEqual(response.status_code, 201)
    
        dict_resp = json.loads(response.content)
        dict_resp_data = dict_resp["data"]
        self.assertEqual(dict_resp_data["type"], "post")
        self.assertEqual(dict_resp_data["title"], "")
        self.assertEqual(dict_resp_data["description"], "")
        self.assertEqual(dict_resp_data["contentType"], f"{Post.ContentTypeEnum.PLAIN}")
        self.assertEqual(dict_resp_data["visibility"], f"{Post.VisibilityEnum.PUBLIC}")
        # Public post uri-id contains its authors id in it
        self.assertIn(str(author.id), dict_resp_data["id"])

    def test_post_post_unauthorized(self):
        """
        should return 403
        """

        user = User(username="username1")
        user.save()
        author: Author = Author.objects.get(userId=user)
        author.save()

        data = {
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
        
        response = self.client.post(reverse('post_api:posts', kwargs={'author_id':author.id}), data, format="json")
        self.assertEqual(response.status_code, 403)

class PostViewTests(TestCase):

    def setUp(self):
        self.auth_helper = AuthHelper()
        self.auth_helper.setup()
        self.client = APIClient()
        self.auth_helper.authorize_client(self.client)

    # ############################################################
    # # TESTS FOR the view class "post"
    # ############################################################
    
    # PUTs #####################

    def test_put_post(self):
        """
        should return the created post
        """

        author = self.auth_helper.get_author()
        postId = uuid4()
        data = {
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
        
        response = self.client.put(reverse(f'post_api:post', kwargs={'author_id':author.id, 'post_id':postId}), data, format="json")
        self.assertEqual(response.status_code, 200)
        
        dict_resp = json.loads(response.content)
        dict_resp_data = dict_resp["data"]
        self.assertEqual(dict_resp_data["type"], data["type"])
        self.assertEqual(dict_resp_data["title"], data["title"])
        self.assertEqual(dict_resp_data["description"], data["description"])
        self.assertEqual(dict_resp_data["contentType"], data["contentType"])
        self.assertEqual(dict_resp_data["visibility"], data["visibility"])
        # Public post uri-id contains its authors id in it
        self.assertIn(str(author.id), dict_resp_data["id"])
    
    def test_put_post_overwrite(self):
        """
        should return 400
        """

        author = self.auth_helper.get_author()
        postId = uuid4()
        data = {
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
        
        response = self.client.put(reverse(f'post_api:post', kwargs={'author_id':author.id, 'post_id':postId}), data, format="json")
        self.assertEqual(response.status_code, 200)
        
        dict_resp = json.loads(response.content)
        dict_resp_data = dict_resp["data"]
        self.assertEqual(dict_resp_data["type"], data["type"])
        self.assertEqual(dict_resp_data["title"], data["title"])
        self.assertEqual(dict_resp_data["description"], data["description"])
        self.assertEqual(dict_resp_data["contentType"], data["contentType"])
        self.assertEqual(dict_resp_data["visibility"], data["visibility"])
        # Public post uri-id contains its authors id in it
        self.assertIn(str(author.id), dict_resp_data["id"])

        data = {
            "type":"post",
            "title":"A different title",
            "description":"TA different desciption",
            "contentType":f"{Post.ContentTypeEnum.APPLICATION}",
            "author":{
                "type":"author",
                "id":f"{author.id}"
            },
            "visibility":f"{Post.VisibilityEnum.FRIENDS}",
            "unlisted":"false"
        }
        
        response = self.client.put(reverse(f'post_api:post', kwargs={'author_id':author.id, 'post_id':postId}), data, format="json")
        self.assertEqual(response.status_code, 400)

    def test_put_post_no_data(self):
        """
        should return a valid, but minimal post
        """

        author = self.auth_helper.get_author()
        postId = uuid4()
        data = {}
        
        response = self.client.put(reverse(f'post_api:post', kwargs={'author_id':author.id, 'post_id':postId}), data, format="json")
        self.assertEqual(response.status_code, 200)
        
        dict_resp = json.loads(response.content)
        dict_resp_data = dict_resp["data"]
        self.assertEqual(dict_resp_data["type"], "post")
        self.assertEqual(dict_resp_data["title"], "")
        self.assertEqual(dict_resp_data["description"], "")
        self.assertEqual(dict_resp_data["contentType"], f"{Post.ContentTypeEnum.PLAIN}")
        self.assertEqual(dict_resp_data["visibility"], f"{Post.VisibilityEnum.PUBLIC}")
        # Public post uri-id contains its authors id in it
        self.assertIn(str(author.id), dict_resp_data["id"])

    def test_put_post_protected_data(self):
        """
        should return the created post with protected fields changed to their correct values
        """

        author = self.auth_helper.get_author()
        postId = uuid4()
        data = {
            "type":"someOtherType",
            "title":"A post title about a post about web dev",
            "description":"This post discusses stuff -- brief",
            "contentType":f"{Post.ContentTypeEnum.MARKDOWN}",
            "author":{
                "type":"someOtherType",
                "id":"someOtherId"
            },
            "visibility":f"{Post.VisibilityEnum.PUBLIC}",
            "unlisted":"false"
        }
        
        response = self.client.put(reverse(f'post_api:post', kwargs={'author_id':author.id, 'post_id':postId}), data, format="json")
        self.assertEqual(response.status_code, 200)
        
        dict_resp = json.loads(response.content)
        dict_resp_data = dict_resp["data"]
        self.assertEqual(dict_resp_data["type"], "post")
        self.assertEqual(dict_resp_data["title"], data["title"])
        self.assertEqual(dict_resp_data["description"], data["description"])
        self.assertEqual(dict_resp_data["contentType"], data["contentType"])
        self.assertEqual(dict_resp_data["visibility"], data["visibility"])
        # Public post uri-id contains its authors id in it
        self.assertIn(str(author.id), dict_resp_data["id"])
        self.assertEqual(dict_resp_data["author"]["type"], "author")
    
    def test_put_post_author_bad_uuid(self):
        """
        should return 403
        """

        author = self.auth_helper.get_author()
        postId = uuid4()
        data = {
            "type":"post",
            "title":"A post title about a post about web dev",
            "description":"This post discusses stuff -- brief",
            "contentType":f"{Post.ContentTypeEnum.MARKDOWN}",
            "author":{
                "type":"author",
                "id":"notARealUUID"
            },
            "visibility":f"{Post.VisibilityEnum.PUBLIC}",
            "unlisted":"false"
        }
        
        response = self.client.put(reverse(f'post_api:post', kwargs={'author_id':"notARealUUID", 'post_id':postId}), data, format="json")
        self.assertEqual(response.status_code, 403)

    def test_put_post_author_nonexist(self):
        """
        should return 403
        """

        authorId = uuid4()
        postId = uuid4()
        data = {
            "type":"post",
            "title":"A post title about a post about web dev",
            "description":"This post discusses stuff -- brief",
            "contentType":"text/markdown",
            "author":{
                "type":"author",
                "id":f"{authorId}"
            },
            "visibility":"PUBLIC",
            "unlisted":"false"
        }
        
        response = self.client.put(reverse(f'post_api:post', kwargs={'author_id':authorId, 'post_id':postId}), data, format="json")
        self.assertEqual(response.status_code, 403)

    # GETs #####################

    def test_get_post(self):
        """
        should return the desired post
        """

        author = self.auth_helper.get_author()
        post = {
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

        response = self.client.post(reverse('post_api:posts', kwargs={'author_id':author.id}), post, format="json")
        self.assertEqual(response.status_code, 201)
        postId = json.loads(response.content)["data"]["id"].split("posts/")[1].rstrip("/")
        response = self.client.get(reverse(f'post_api:post', kwargs={'author_id':author.id, 'post_id':postId}))
        self.assertEqual(response.status_code, 200)
        
        dict_resp = json.loads(response.content)
        dict_resp_data = dict_resp["data"]
        self.assertEqual(dict_resp_data["type"], post["type"])
        self.assertEqual(dict_resp_data["title"], post["title"])
        self.assertEqual(dict_resp_data["description"], post["description"])
        self.assertEqual(dict_resp_data["contentType"], post["contentType"])
        self.assertEqual(dict_resp_data["visibility"], post["visibility"])
        # Public post uri-id contains its authors id in it
        self.assertIn(str(author.id), dict_resp_data["id"])

    def test_get_post_bad_uuid(self):
        """
        should return the desired post
        """

        author = self.auth_helper.get_author()
        post = {
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

        response = self.client.post(reverse('post_api:posts', kwargs={'author_id':author.id}), post, format="json")
        self.assertEqual(response.status_code, 201)
        response = self.client.get(reverse(f'post_api:post', kwargs={'author_id':author.id, 'post_id':"notARealUUID"}))
        self.assertEqual(response.status_code, 404)

    def test_get_post_author_nonexist(self):
        """
        should return 404
        """

        author = self.auth_helper.get_author()
        authorId = uuid4()
        post = {
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

        response = self.client.post(reverse('post_api:posts', kwargs={'author_id':author.id}), post, format="json")
        self.assertEqual(response.status_code, 201)
        postId = json.loads(response.content)["data"]["id"].split("posts/")[1].rstrip("/")
        response = self.client.get(reverse(f'post_api:post', kwargs={'author_id':authorId, 'post_id':postId}))
        self.assertEqual(response.status_code, 404)

    def test_get_post_nonexist(self):
        """
        should return 404
        """
        
        author = self.auth_helper.get_author()
        postId = uuid4()
        response = self.client.get(reverse(f'post_api:post', kwargs={'author_id':author.id, 'post_id':postId}))
        self.assertEqual(response.status_code, 404)

    # POSTs ####################

    def test_post_post(self):
        """
        should return the modified post, and not create another one
        """

        author = self.auth_helper.get_author()
        oldData = {
            "type":"post",
            "title":"TITLE",
            "description":"DESC",
            "contentType":f"{Post.ContentTypeEnum.PLAIN}",
            "author":{
                "type":"author",
                "id":f"{author.id}"
            },
            "visibility":f"{Post.VisibilityEnum.FRIENDS}",
            "unlisted":"false"
        }
        postId = uuid4()

        response = self.client.put(reverse(f'post_api:post', kwargs={'author_id':author.id, 'post_id':postId}), oldData, format="json")
        self.assertEqual(response.status_code, 200)

        data = {
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
        
        response = self.client.post(reverse(f'post_api:post', kwargs={'author_id':author.id, 'post_id':postId}), data, format="json")
        self.assertEqual(response.status_code, 200)
        response = self.client.get(reverse(f'post_api:posts', kwargs={'author_id':author.id}))
        self.assertEqual(response.status_code, 200)

        dict_resp = json.loads(response.content)
        self.assertEqual(len(dict_resp["data"]), 1)
        dict_resp_data = dict_resp["data"][0]

        self.assertEqual(dict_resp_data["type"], data["type"])
        self.assertEqual(dict_resp_data["title"], data["title"])
        self.assertEqual(dict_resp_data["description"], data["description"])
        self.assertEqual(dict_resp_data["contentType"], data["contentType"])
        self.assertEqual(dict_resp_data["visibility"], data["visibility"])
        # Public post uri-id contains its authors id in it
        self.assertIn(str(author.id), dict_resp_data["id"])

        retPost = Post.objects.get(id=postId)
        self.assertEqual(retPost.title, data["title"])
        self.assertEqual(retPost.description, data["description"])
        self.assertEqual(str(retPost.contentType), data["contentType"])
        self.assertEqual(str(retPost.visibility), data["visibility"])
        # Public post uri-id contains its authors id in it
        self.assertIn(str(author.id), dict_resp_data["id"])

    def test_post_post_nonexist(self):
        """
        should return 404
        """

        author = self.auth_helper.get_author()
        data = {
            "type":"post",
            "title":"TITLE",
            "description":"DESC",
            "contentType":f"{Post.ContentTypeEnum.PLAIN}",
            "author":{
                "type":"author",
                "id":f"{author.id}"
            },
            "visibility":f"{Post.VisibilityEnum.FRIENDS}",
            "unlisted":"false"
        }
        postId = uuid4()
        
        response = self.client.post(reverse(f'post_api:post', kwargs={'author_id':author.id, 'post_id':postId}), data, format="json")
        self.assertEqual(response.status_code, 404)

    def test_post_post_bad_uuid(self):
        """
        should return 404
        """

        author = self.auth_helper.get_author()
        data = {
            "type":"post",
            "title":"TITLE",
            "description":"DESC",
            "contentType":f"{Post.ContentTypeEnum.PLAIN}",
            "author":{
                "type":"author",
                "id":f"{author.id}"
            },
            "visibility":f"{Post.VisibilityEnum.FRIENDS}",
            "unlisted":"false"
        }
        postId = "notARealUUID"
        
        response = self.client.post(reverse(f'post_api:post', kwargs={'author_id':author.id, 'post_id':postId}), data, format="json")
        self.assertEqual(response.status_code, 404)

    def test_post_post_author_nonexist(self):
        """
        should return 403
        """

        author = self.auth_helper.get_author()
        authorId = uuid4()
        data = {
            "type":"post",
            "title":"TITLE",
            "description":"DESC",
            "contentType":f"{Post.ContentTypeEnum.PLAIN}",
            "author":{
                "type":"author",
                "id":f"{author.id}"
            },
            "visibility":f"{Post.VisibilityEnum.FRIENDS}",
            "unlisted":"false"
        }
        postId = uuid4()

        response = self.client.put(reverse(f'post_api:post', kwargs={'author_id':author.id, 'post_id':postId}), data, format="json")
        self.assertEqual(response.status_code, 200)
        
        response = self.client.post(reverse(f'post_api:post', kwargs={'author_id':authorId, 'post_id':postId}), data, format="json")
        self.assertEqual(response.status_code, 403)

    def test_post_post_no_data(self):
        """
        should return the modified post, and not create another one
        """

        author = self.auth_helper.get_author()
        oldData = {
            "type":"post",
            "title":"TITLE",
            "description":"DESC",
            "contentType":f"{Post.ContentTypeEnum.PLAIN}",
            "author":{
                "type":"author",
                "id":f"{author.id}"
            },
            "visibility":f"{Post.VisibilityEnum.FRIENDS}",
            "unlisted":"false"
        }
        postId = uuid4()

        response = self.client.put(reverse(f'post_api:post', kwargs={'author_id':author.id, 'post_id':postId}), oldData, format="json")
        self.assertEqual(response.status_code, 200)

        data = {}
        
        response = self.client.post(reverse(f'post_api:post', kwargs={'author_id':author.id, 'post_id':postId}), data, format="json")
        self.assertEqual(response.status_code, 200)
        response = self.client.get(reverse(f'post_api:posts', kwargs={'author_id':author.id}))
        self.assertEqual(response.status_code, 200)

        dict_resp = json.loads(response.content)
        self.assertEqual(len(dict_resp["data"]), 1)
        dict_resp_data = dict_resp["data"][0]

        self.assertEqual(dict_resp_data["type"], oldData["type"])
        self.assertEqual(dict_resp_data["title"], oldData["title"])
        self.assertEqual(dict_resp_data["description"], oldData["description"])
        self.assertEqual(dict_resp_data["contentType"], oldData["contentType"])
        self.assertEqual(dict_resp_data["visibility"], oldData["visibility"])
        # Public post uri-id contains its authors id in it
        self.assertIn(str(author.id), dict_resp_data["id"])

        retPost = Post.objects.get(id=postId)
        self.assertEqual(retPost.title, oldData["title"])
        self.assertEqual(retPost.description, oldData["description"])
        self.assertEqual(str(retPost.contentType), oldData["contentType"])
        self.assertEqual(str(retPost.visibility), oldData["visibility"])
        # Public post uri-id contains its authors id in it
        self.assertIn(str(author.id), dict_resp_data["id"])

    def test_post_change_protected_data(self):
        """
        should return the unchanged post with protected fields staying their correct values
        """

        author = self.auth_helper.get_author()
        oldData = {
            "type":"post",
            "title":"TITLE",
            "description":"DESC",
            "contentType":f"{Post.ContentTypeEnum.PLAIN}",
            "author":{
                "type":"author",
                "id":f"{author.id}"
            },
            "visibility":f"{Post.VisibilityEnum.FRIENDS}",
            "unlisted":"false"
        }
        postId = uuid4()

        response = self.client.put(reverse(f'post_api:post', kwargs={'author_id':author.id, 'post_id':postId}), oldData, format="json")
        self.assertEqual(response.status_code, 200)

        data = {
            "type":"someOtherType",
            "author":{
                "type":"someOtherType",
                "id":"someOtherId"
            },
        }
        
        response = self.client.post(reverse(f'post_api:post', kwargs={'author_id':author.id, 'post_id':postId}), data, format="json")
        self.assertEqual(response.status_code, 200)
        response = self.client.get(reverse(f'post_api:posts', kwargs={'author_id':author.id}))
        self.assertEqual(response.status_code, 200)

        dict_resp = json.loads(response.content)
        self.assertEqual(len(dict_resp["data"]), 1)
        dict_resp_data = dict_resp["data"][0]

        self.assertEqual(dict_resp_data["type"], oldData["type"])
        self.assertEqual(dict_resp_data["title"], oldData["title"])
        self.assertEqual(dict_resp_data["description"], oldData["description"])
        self.assertEqual(dict_resp_data["contentType"], oldData["contentType"])
        self.assertEqual(dict_resp_data["visibility"], oldData["visibility"])
        # Public post uri-id contains its authors id in it
        self.assertIn(str(author.id), dict_resp_data["id"])
        self.assertEqual(dict_resp_data["author"]["type"], "author")

    # DELETEs ##################

    def test_delete_post(self):
        """
        should return 204, and a get on the post should yield 404
        """

        author = self.auth_helper.get_author()
        title = "TITLE"
        description = "DESC"
        contentType = Post.ContentTypeEnum.PLAIN
        visibility = Post.VisibilityEnum.PUBLIC
        post = Post.objects.create(title=title, description=description, contentType=contentType, visibility=visibility, author=author)
        post.save()

        postId = post.id

        response = self.client.get(reverse(f'post_api:post', kwargs={'author_id':author.id, 'post_id':postId}))
        self.assertEqual(response.status_code, 200)
        response = self.client.delete(reverse(f'post_api:post', kwargs={'author_id':author.id, 'post_id':postId}), format="json")
        self.assertEqual(response.status_code, 204)
        response = self.client.get(reverse(f'post_api:post', kwargs={'author_id':author.id, 'post_id':postId}))
        self.assertEqual(response.status_code, 404)

    def test_delete_post_nonexist(self):
        """
        should return 404
        """
        
        author = self.auth_helper.get_author()
        postId = uuid4()
        response = self.client.delete(reverse(f'post_api:post', kwargs={'author_id':author.id, 'post_id':postId}), format="json")
        self.assertEqual(response.status_code, 404)

    def test_delete_post_author_nonexist(self):
        """
        should return 403
        """
        
        author = self.auth_helper.get_author()
        postId = uuid4()
        data = {
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

        response = self.client.put(reverse(f'post_api:post', kwargs={'author_id':author.id, 'post_id':postId}), data, format="json")
        self.assertEqual(response.status_code, 200)

        authorId = uuid4()
        
        response = self.client.delete(reverse(f'post_api:post', kwargs={'author_id':authorId, 'post_id':postId}), format="json")
        self.assertEqual(response.status_code, 403)

class CommentViewTests(TestCase):

    def setUp(self):
        self.auth_helper = AuthHelper()
        self.auth_helper.setup()
        self.client = APIClient()
        self.auth_helper.authorize_client(self.client)

    # POSTs ####################

    def test_post_comment(self):
        """
        should return the created comment
        """
        
        author = self.auth_helper.get_author()

        data = {
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
        
        response = self.client.post(reverse('post_api:posts', kwargs={'author_id':author.id}), data, format="json")
        self.assertEqual(response.status_code, 201)
        postId = json.loads(response.content)["data"]["id"].split("posts/")[1].rstrip("/")

        comment_data = {
            "type":"comment",
            "author":{
                "type":"author",
                "id":f"{author.id}"
            },
            "comment":"A Comment with words and markdown",
            "contentType":f"{Comment.ContentTypeEnum.MARKDOWN}"
        }

        response = self.client.post(reverse('post_api:comments', kwargs={'author_id':author.id, 'post_id':postId}), comment_data, format="json")
        self.assertEqual(response.status_code, 201)
        dict_resp_data = json.loads(response.content)["data"]
        self.assertEqual(dict_resp_data["type"], comment_data["type"])
        self.assertEqual(dict_resp_data["comment"], comment_data["comment"])
        self.assertEqual(dict_resp_data["contentType"], comment_data["contentType"])
        self.assertEqual(dict_resp_data["author"]["id"], str(author.id))

    def test_post_comment_no_data(self):
        """
        should create a minimal comment with default values where applicable
        """
        
        author = self.auth_helper.get_author()

        post = {
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
        
        response = self.client.post(reverse('post_api:posts', kwargs={'author_id':author.id}), post, format="json")
        self.assertEqual(response.status_code, 201)
        postId = json.loads(response.content)["data"]["id"].split("posts/")[1].rstrip("/")

        comment_data = {}

        response = self.client.post(reverse('post_api:comments', kwargs={'author_id':author.id, 'post_id':postId}), comment_data, format="json")
        self.assertEqual(response.status_code, 201)

        response = self.client.get(reverse('post_api:comments', kwargs={'author_id':author.id, 'post_id':postId}))
        self.assertEqual(response.status_code, 200)

        dict_resp_data = json.loads(response.content)["data"]
        self.assertEquals(len(dict_resp_data), 1)

        data = dict_resp_data[0]
        self.assertEqual(data["type"], "comment")
        self.assertEqual(data["comment"], "")
        self.assertEqual(data["contentType"], f"{Comment.ContentTypeEnum.PLAIN}")
        self.assertEqual(data["author"]["id"], str(author.id))

    def test_post_comments_protected_data(self):
        """
        should return the created comment with protected fields changed to their correct values
        """
        
        author = self.auth_helper.get_author()

        post = {
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
        
        response = self.client.post(reverse('post_api:posts', kwargs={'author_id':author.id}), post, format="json")
        self.assertEqual(response.status_code, 201)
        postId = json.loads(response.content)["data"]["id"].split("posts/")[1].rstrip("/")

        comment_data = {
            "type":"someOtherType",
            "author":{
                "type":"someOtherType",
                "id":"notARealUUID"
            },
            "comment":"A Comment with words and markdown",
            "contentType":f"{Comment.ContentTypeEnum.MARKDOWN}"
        }

        response = self.client.post(reverse('post_api:comments', kwargs={'author_id':author.id, 'post_id':postId}), comment_data, format="json")
        self.assertEqual(response.status_code, 201)

        response = self.client.get(reverse('post_api:comments', kwargs={'author_id':author.id, 'post_id':postId}))
        self.assertEqual(response.status_code, 200)

        dict_resp_data = json.loads(response.content)["data"]
        self.assertEquals(len(dict_resp_data), 1)

        data = dict_resp_data[0]
        self.assertEqual(data["type"], "comment")
        self.assertEqual(data["comment"], comment_data["comment"])
        self.assertEqual(data["contentType"], comment_data["contentType"])
        self.assertEqual(data["author"]["id"], str(author.id))
        self.assertEqual(data["author"]["type"], "author")

    # GETs #####################

    def test_get_comments_no_posts(self):
        """
        should return an empty list
        """
        
        author = self.auth_helper.get_author()
        postId = uuid4()
        response = self.client.get(reverse('post_api:comments', kwargs={'author_id':author.id, 'post_id':postId}))
        self.assertEqual(response.status_code, 200)
        self.assertEquals(len(json.loads(response.content)["data"]), 0)

    def test_get_comments(self):
        """
        should return all created comments
        """
        
        author = self.auth_helper.get_author()

        post = {
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
        
        response = self.client.post(reverse('post_api:posts', kwargs={'author_id':author.id}), post, format="json")
        self.assertEqual(response.status_code, 201)
        postId = json.loads(response.content)["data"]["id"].split("posts/")[1].rstrip("/")

        comment_data = {
            "type":"comment",
            "author":{
                "type":"author",
                "id":f"{author.id}"
            },
            "comment":"A Comment with words and markdown",
            "contentType":f"{Comment.ContentTypeEnum.MARKDOWN}"
        }

        comment_data2 = {
            "type":"comment",
            "author":{
                "type":"author",
                "id":f"{author.id}"
            },
            "comment":"A Different Comment!",
            "contentType":f"{Comment.ContentTypeEnum.PLAIN}"
        }

        response = self.client.post(reverse('post_api:comments', kwargs={'author_id':author.id, 'post_id':postId}), comment_data, format="json")
        self.assertEqual(response.status_code, 201)
        response = self.client.post(reverse('post_api:comments', kwargs={'author_id':author.id, 'post_id':postId}), comment_data2, format="json")
        self.assertEqual(response.status_code, 201)
        response = self.client.get(reverse('post_api:comments', kwargs={'author_id':author.id, 'post_id':postId}))
        self.assertEqual(response.status_code, 200)

        dict_resp_data = json.loads(response.content)["data"]
        self.assertEquals(len(dict_resp_data), 2)

        data1 = dict_resp_data[0]
        data2 = dict_resp_data[1]

        if(data1["comment"] != comment_data["comment"]):
            temp = data2
            data2 = data1
            data1 = temp
        
        self.assertEqual(data1["type"], comment_data["type"])
        self.assertEqual(data1["comment"], comment_data["comment"])
        self.assertEqual(data1["contentType"], comment_data["contentType"])
        self.assertEqual(data1["author"]["id"], str(author.id))

        self.assertEqual(data2["type"], comment_data2["type"])
        self.assertEqual(data2["comment"], comment_data2["comment"])
        self.assertEqual(data2["contentType"], comment_data2["contentType"])
        self.assertEqual(data2["author"]["id"], str(author.id))

    def test_get_comments_author_nonexist(self):
        """
        should return 404
        """
        
        author = self.auth_helper.get_author()

        post = {
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
        
        response = self.client.post(reverse('post_api:posts', kwargs={'author_id':author.id}), post, format="json")
        self.assertEqual(response.status_code, 201)
        postId = json.loads(response.content)["data"]["id"].split("posts/")[1].rstrip("/")

        comment_data = {
            "type":"comment",
            "author":{
                "type":"author",
                "id":f"{author.id}"
            },
            "comment":"A Comment with words and markdown",
            "contentType":f"{Comment.ContentTypeEnum.MARKDOWN}"
        }

        authorId = uuid4()

        response = self.client.post(reverse('post_api:comments', kwargs={'author_id':authorId, 'post_id':postId}), comment_data, format="json")
        self.assertEqual(response.status_code, 404)

    def test_get_comments_bad_uuid(self):
        """
        should return 404
        """
        
        author = self.auth_helper.get_author()

        post = {
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
        
        response = self.client.post(reverse('post_api:posts', kwargs={'author_id':author.id}), post, format="json")
        self.assertEqual(response.status_code, 201)
        postId = json.loads(response.content)["data"]["id"].split("posts/")[1].rstrip("/")

        comment_data = {
            "type":"comment",
            "author":{
                "type":"author",
                "id":f"{author.id}"
            },
            "comment":"A Comment with words and markdown",
            "contentType":f"{Comment.ContentTypeEnum.MARKDOWN}"
        }

        authorId = "notARealUUID"

        response = self.client.post(reverse('post_api:comments', kwargs={'author_id':authorId, 'post_id':postId}), comment_data, format="json")
        self.assertEqual(response.status_code, 404)