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

        self.assertEqual(response.status_code, 200, f"expected 200. got: {response.status_code}")
        dict_resp = json.loads(response.content)

        # checking default pagination
        self.assertEqual(dict_resp["page"], DEFAULT_PAGE, f"expected page {DEFAULT_PAGE}. got: {dict_resp['page']}")
        self.assertEqual(dict_resp["size"], DEFAULT_PAGE_SIZE, f"expected page size {DEFAULT_PAGE_SIZE}. got: {dict_resp['size']}")

        self.assertEqual(len(dict_resp["data"]), 0, "list should have been empty but wasn't!")

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
        self.assertEqual(response.status_code, 201, f"expected 201. got: {response.status_code}")
        response = self.client.post(reverse('post_api:posts', kwargs={'author_id':author.id}), post2, format="json")
        self.assertEqual(response.status_code, 201, f"expected 201. got: {response.status_code}")
        response = self.client.get(reverse('post_api:posts', kwargs={'author_id':author.id}))
        self.assertEqual(response.status_code, 200, f"expected 200. got: {response.status_code}")
        dict_resp = json.loads(response.content)
        dict_resp_data = dict_resp["data"]

        # checking default pagination
        self.assertEqual(dict_resp["page"], DEFAULT_PAGE, f"expected page {DEFAULT_PAGE}. got: {dict_resp['page']}")
        self.assertEqual(dict_resp["size"], DEFAULT_PAGE_SIZE, f"expected page size {DEFAULT_PAGE_SIZE}. got: {dict_resp['size']}")

        self.assertEqual(len(dict_resp_data), 2, f"expected list of length 2. got: {len(dict_resp_data)}")

        data1 = dict_resp_data[0]
        data2 = dict_resp_data[1]

        if(data1["title"] != post1["title"]):
            temp = data2
            data2 = data1
            data1 = temp

        self.assertEqual(data1["type"], post1["type"], "returned item had wrong type!")
        self.assertEqual(data1["title"], post1["title"], "returned item had wrong title!")
        self.assertEqual(data1["description"], post1["description"], "returned item had wrong description!")
        self.assertEqual(data1["contentType"], post1["contentType"], "returned item had wrong contentType!")
        self.assertEqual(data1["visibility"], post1["visibility"], "returned item had wrong visibility!")
        # Public post uri-id contains its authors id in it
        self.assertIn(str(author.id), data1["id"], "returned item referenced wrong author!")

        self.assertEqual(data2["type"], post2["type"], "returned item had wrong type!")
        self.assertEqual(data2["title"], post2["title"], "returned item had wrong title!")
        self.assertEqual(data2["description"], post2["description"], "returned item had wrong description!")
        self.assertEqual(data2["contentType"], post2["contentType"], "returned item had wrong contentType!")
        self.assertEqual(data2["visibility"], post2["visibility"], "returned item had wrong visibility!")
        # Public post uri-id contains its authors id in it
        self.assertIn(str(author.id), data2["id"], "returned item referenced wrong author!")

    def test_get_posts_access_levels(self):
        """
        should return 200 for all users
        """
        
        password = "password"
        user = User.objects.create_user("username1", password=password)
        author: Author = Author.objects.get(userId=user)
        self.client.logout()
        self.client.login(username=user.username, password=password)

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

        response = self.client.post(reverse('post_api:posts', kwargs={'author_id':author.id}), post1, format="json")
        self.assertEqual(response.status_code, 201, f"expected 201. got: {response.status_code}")

        # test anonymous user
        self.client.logout()
        response = self.client.get(reverse('post_api:posts', kwargs={'author_id':author.id}))
        self.assertEqual(response.status_code, 200, f"expected 200. got: {response.status_code}")
        # test non participant
        self.client.logout()
        nonParticipant = User.objects.create_user("nonParticipant", password=password)
        self.assertTrue(self.client.login(username=nonParticipant.username, password=password))
        response = self.client.get(reverse('post_api:posts', kwargs={'author_id':author.id}))
        self.assertEqual(response.status_code, 200, f"expected 200. got: {response.status_code}")
        # test owner
        self.client.logout()
        self.assertTrue(self.client.login(username=user.username, password=password))
        response = self.client.get(reverse('post_api:posts', kwargs={'author_id':author.id}))
        self.assertEqual(response.status_code, 200, f"expected 200. got: {response.status_code}")
        # test admin
        self.client.logout()
        self.auth_helper.authorize_client(self.client)
        response = self.client.get(reverse('post_api:posts', kwargs={'author_id':author.id}))
        self.assertEqual(response.status_code, 200, f"expected 200. got: {response.status_code}")
        
    def test_get_posts_bad_uuid(self):
        """
        should return 404
        """

        response = self.client.get(reverse('post_api:posts', kwargs={'author_id':'notARealUUID'}))
        self.assertEqual(response.status_code, 404, f"expected 404. got: {response.status_code}")

    def test_get_posts_author_nonexist(self):
        """
        should return 404
        """

        response = self.client.get(reverse('post_api:posts', kwargs={'author_id': '0b552c30-0a2e-445e-828d-b356b5276c0f'}))
        self.assertEqual(response.status_code, 404, f"expected 404. got: {response.status_code}")

    def test_get_posts_multiple_authors(self):
        """
        should only return posts from the correct author
        """
        
        author = self.auth_helper.get_author()
        password = "password"
        user2 = User.objects.create_user("username2", password=password)
        author2: Author = Author.objects.get(userId=user2)
        
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
                "id":f"{author2.id}"
            },
            "visibility":f"{Post.VisibilityEnum.FRIENDS}",
            "unlisted":"false"
        }

        response = self.client.post(reverse('post_api:posts', kwargs={'author_id':author.id}), post1, format="json")
        self.assertEqual(response.status_code, 201)
        self.client.logout()
        self.assertTrue(self.client.login(username=user2.username, password=password))
        response = self.client.post(reverse('post_api:posts', kwargs={'author_id':author2.id}), post2, format="json")
        self.assertEqual(response.status_code, 201)
        response = self.client.get(reverse('post_api:posts', kwargs={'author_id':author.id}))
        self.assertEqual(response.status_code, 200)
        dict_resp = json.loads(response.content)
        dict_resp_data = dict_resp["data"][0]

        # checking default pagination
        self.assertEqual(dict_resp["page"], DEFAULT_PAGE)
        self.assertEqual(dict_resp["size"], DEFAULT_PAGE_SIZE)
        # print(dict_resp_data)

        self.assertEqual(dict_resp_data["type"], post1["type"])
        self.assertEqual(dict_resp_data["title"], post1["title"])
        self.assertEqual(dict_resp_data["description"], post1["description"])
        self.assertEqual(dict_resp_data["contentType"], post1["contentType"])
        self.assertEqual(dict_resp_data["visibility"], post1["visibility"])
        # Public post uri-id contains its authors id in it
        self.assertIn(str(author.id), dict_resp_data["id"])

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
        self.assertEqual(response.status_code, 201, f"expected 201. got: {response.status_code}")
    
        dict_resp = json.loads(response.content)
        dict_resp_data = dict_resp["data"]
        self.assertEqual(dict_resp_data["type"], data["type"], "returned item had wrong type!")
        self.assertEqual(dict_resp_data["title"], data["title"], "returned item had wrong title!")
        self.assertEqual(dict_resp_data["description"], data["description"], "returned item had wrong description!")
        self.assertEqual(dict_resp_data["contentType"], data["contentType"], "returned item had wrong contentType!")
        self.assertEqual(dict_resp_data["visibility"], data["visibility"], "returned item had wrong visibility!")
        # Public post uri-id contains its authors id in it
        self.assertIn(str(author.id), dict_resp_data["id"], "returned item referenced wrong author!")

    def test_post_post_access_levels(self):
        """
        should return 403 for all users but the owner
        """

        password = "password"
        user = User.objects.create_user("username1", password=password)
        author: Author = Author.objects.get(userId=user)
        self.client.logout()
        self.client.login(username=user.username, password=password)

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
        self.assertEqual(response.status_code, 201, f"expected 201. got: {response.status_code}")

        # test anonymous user
        self.client.logout()
        response = self.client.post(reverse('post_api:posts', kwargs={'author_id':author.id}), data, format="json")
        self.assertEqual(response.status_code, 403, f"expected 403. got: {response.status_code}")
        # test non participant
        self.client.logout()
        nonParticipant = User.objects.create_user("nonParticipant", password=password)
        self.assertTrue(self.client.login(username=nonParticipant.username, password=password))
        response = self.client.post(reverse('post_api:posts', kwargs={'author_id':author.id}), data, format="json")
        self.assertEqual(response.status_code, 403, f"expected 403. got: {response.status_code}")
        # test owner
        self.client.logout()
        self.assertTrue(self.client.login(username=user.username, password=password))
        response = self.client.post(reverse('post_api:posts', kwargs={'author_id':author.id}), data, format="json")
        self.assertEqual(response.status_code, 201, f"expected 201. got: {response.status_code}")
        # test admin
        self.client.logout()
        self.auth_helper.authorize_client(self.client)
        response = self.client.post(reverse('post_api:posts', kwargs={'author_id':author.id}), data, format="json")
        self.assertEqual(response.status_code, 403, f"expected 403. got: {response.status_code}")

    def test_post_post_no_data(self):
        """
        should return the created post
        """

        author = self.auth_helper.get_author()

        data = {}
        
        response = self.client.post(reverse('post_api:posts', kwargs={'author_id':author.id}), data, format="json")
        self.assertEqual(response.status_code, 201, f"expected 201. got: {response.status_code}")
    
        dict_resp = json.loads(response.content)
        dict_resp_data = dict_resp["data"]
        self.assertEqual(dict_resp_data["type"], "post", "returned item had wrong type!")
        self.assertEqual(dict_resp_data["title"], "", "returned item had wrong title!")
        self.assertEqual(dict_resp_data["description"], "", "returned item had wrong description!")
        self.assertEqual(dict_resp_data["contentType"], f"{Post.ContentTypeEnum.PLAIN}", "returned item had wrong contentType!")
        self.assertEqual(dict_resp_data["visibility"], f"{Post.VisibilityEnum.PUBLIC}", "returned item had wrong visibility!")
        # Public post uri-id contains its authors id in it
        self.assertIn(str(author.id), dict_resp_data["id"], "returned item referenced wrong author!")

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
        self.assertEqual(response.status_code, 403, f"expected 403. got: {response.status_code}")

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
        
        response = self.client.put(reverse('post_api:post', kwargs={'author_id':author.id, 'post_id':postId}), data, format="json")
        self.assertEqual(response.status_code, 201, f"expected 201. got: {response.status_code}")
        
        dict_resp = json.loads(response.content)
        dict_resp_data = dict_resp["data"]
        self.assertEqual(dict_resp_data["type"], data["type"], "returned item had wrong type!")
        self.assertEqual(dict_resp_data["title"], data["title"], "returned item had wrong title!")
        self.assertEqual(dict_resp_data["description"], data["description"], "returned item had wrong description!")
        self.assertEqual(dict_resp_data["contentType"], data["contentType"], "returned item had wrong contentType!")
        self.assertEqual(dict_resp_data["visibility"], data["visibility"], "returned item had wrong visibility!")
        # Public post uri-id contains its authors id in it
        self.assertIn(str(author.id), dict_resp_data["id"], "returned item referenced wrong author!")

    def test_put_post_access_levels(self):
        """
        should return 403 for all users except owner
        """

        password = "password"
        user = User.objects.create_user("username1", password=password)
        author: Author = Author.objects.get(userId=user)
        self.client.logout()
        self.client.login(username=user.username, password=password)
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
        
        # test anonymous user
        self.client.logout()
        response = self.client.put(reverse('post_api:post', kwargs={'author_id':author.id, 'post_id':postId}), data, format="json")
        self.assertEqual(response.status_code, 403, f"expected 403. got: {response.status_code}")
        # test non participant
        self.client.logout()
        nonParticipant = User.objects.create_user("nonParticipant", password=password)
        self.assertTrue(self.client.login(username=nonParticipant.username, password=password))
        response = self.client.put(reverse('post_api:post', kwargs={'author_id':author.id, 'post_id':postId}), data, format="json")
        self.assertEqual(response.status_code, 403, f"expected 403. got: {response.status_code}")
        # test owner
        self.client.logout()
        self.assertTrue(self.client.login(username=user.username, password=password))
        response = self.client.put(reverse('post_api:post', kwargs={'author_id':author.id, 'post_id':postId}), data, format="json")
        self.assertEqual(response.status_code, 201, f"expected 201. got: {response.status_code}")
        # test admin
        self.client.logout()
        self.auth_helper.authorize_client(self.client)
        response = self.client.put(reverse('post_api:post', kwargs={'author_id':author.id, 'post_id':postId}), data, format="json")
        self.assertEqual(response.status_code, 403, f"expected 403. got: {response.status_code}")
        
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
        
        response = self.client.put(reverse('post_api:post', kwargs={'author_id':author.id, 'post_id':postId}), data, format="json")
        self.assertEqual(response.status_code, 201, f"expected 201. got: {response.status_code}")
        
        dict_resp = json.loads(response.content)
        dict_resp_data = dict_resp["data"]
        self.assertEqual(dict_resp_data["type"], data["type"], "returned item had wrong type!")
        self.assertEqual(dict_resp_data["title"], data["title"], "returned item had wrong title!")
        self.assertEqual(dict_resp_data["description"], data["description"], "returned item had wrong description!")
        self.assertEqual(dict_resp_data["contentType"], data["contentType"], "returned item had wrong contentType!")
        self.assertEqual(dict_resp_data["visibility"], data["visibility"], "returned item had wrong visibility!")
        # Public post uri-id contains its authors id in it
        self.assertIn(str(author.id), dict_resp_data["id"], "returned item referenced wrong author!")

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
        
        response = self.client.put(reverse('post_api:post', kwargs={'author_id':author.id, 'post_id':postId}), data, format="json")
        self.assertEqual(response.status_code, 400, f"expected 400. got: {response.status_code}")

    def test_put_post_no_data(self):
        """
        should return a valid, but minimal post
        """

        author = self.auth_helper.get_author()
        postId = uuid4()
        data = {}
        
        response = self.client.put(reverse('post_api:post', kwargs={'author_id':author.id, 'post_id':postId}), data, format="json")
        self.assertEqual(response.status_code, 201, f"expected 201. got: {response.status_code}")
        
        dict_resp = json.loads(response.content)
        dict_resp_data = dict_resp["data"]
        self.assertEqual(dict_resp_data["type"], "post", "returned item had wrong type!")
        self.assertEqual(dict_resp_data["title"], "", "returned item had wrong title!")
        self.assertEqual(dict_resp_data["description"], "", "returned item had wrong description!")
        self.assertEqual(dict_resp_data["contentType"], f"{Post.ContentTypeEnum.PLAIN}", "returned item had wrong contentType!")
        self.assertEqual(dict_resp_data["visibility"], f"{Post.VisibilityEnum.PUBLIC}", "returned item had wrong visibility!")
        # Public post uri-id contains its authors id in it
        self.assertIn(str(author.id), dict_resp_data["id"], "returned item referenced wrong author!")

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
        
        response = self.client.put(reverse('post_api:post', kwargs={'author_id':author.id, 'post_id':postId}), data, format="json")
        self.assertEqual(response.status_code, 201, f"expected 201. got: {response.status_code}")
        
        dict_resp = json.loads(response.content)
        dict_resp_data = dict_resp["data"]
        self.assertEqual(dict_resp_data["type"], "post", "returned item had wrong type!")
        self.assertEqual(dict_resp_data["title"], data["title"], "returned item had wrong title!")
        self.assertEqual(dict_resp_data["description"], data["description"], "returned item had wrong description!")
        self.assertEqual(dict_resp_data["contentType"], data["contentType"], "returned item had wrong contentType!")
        self.assertEqual(dict_resp_data["visibility"], data["visibility"], "returned item had wrong visibility!")
        # Public post uri-id contains its authors id in it
        self.assertIn(str(author.id), dict_resp_data["id"], "returned item referenced wrong author!")
        self.assertEqual(dict_resp_data["author"]["type"], "author", "returned item does not have an author object!")
    
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
        
        response = self.client.put(reverse('post_api:post', kwargs={'author_id':"notARealUUID", 'post_id':postId}), data, format="json")
        self.assertEqual(response.status_code, 403, f"expected 403. got: {response.status_code}")

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
        
        response = self.client.put(reverse('post_api:post', kwargs={'author_id':authorId, 'post_id':postId}), data, format="json")
        self.assertEqual(response.status_code, 403, f"expected 403. got: {response.status_code}")

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
        self.assertEqual(response.status_code, 201, f"expected 201. got: {response.status_code}")
        postId = json.loads(response.content)["data"]["id"].split("posts/")[1].rstrip("/")
        response = self.client.get(reverse('post_api:post', kwargs={'author_id':author.id, 'post_id':postId}))
        self.assertEqual(response.status_code, 200, f"expected 200. got: {response.status_code}")
        
        dict_resp = json.loads(response.content)
        dict_resp_data = dict_resp["data"]
        self.assertEqual(dict_resp_data["type"], post["type"], "returned item had wrong type!")
        self.assertEqual(dict_resp_data["title"], post["title"], "returned item had wrong title!")
        self.assertEqual(dict_resp_data["description"], post["description"], "returned item had wrong description!")
        self.assertEqual(dict_resp_data["contentType"], post["contentType"], "returned item had wrong contentType!")
        self.assertEqual(dict_resp_data["visibility"], post["visibility"], "returned item had wrong visibility!")
        # Public post uri-id contains its authors id in it
        self.assertIn(str(author.id), dict_resp_data["id"], "returned item referenced wrong author!")

    def test_get_post_access_levels(self):
        """
        should return 200 for all users
        """

        password = "password"
        user = User.objects.create_user("username1", password=password)
        author: Author = Author.objects.get(userId=user)
        self.client.logout()
        self.client.login(username=user.username, password=password)
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
        self.assertEqual(response.status_code, 201, f"expected 201. got: {response.status_code}")
        postId = json.loads(response.content)["data"]["id"].split("posts/")[1].rstrip("/")
        
        # test anonymous user
        self.client.logout()
        response = self.client.get(reverse('post_api:post', kwargs={'author_id':author.id, 'post_id':postId}))
        self.assertEqual(response.status_code, 200, f"expected 200. got: {response.status_code}")
        # test non participant
        self.client.logout()
        nonParticipant = User.objects.create_user("nonParticipant", password=password)
        self.assertTrue(self.client.login(username=nonParticipant.username, password=password))
        response = self.client.get(reverse('post_api:post', kwargs={'author_id':author.id, 'post_id':postId}))
        self.assertEqual(response.status_code, 200, f"expected 200. got: {response.status_code}")
        # test owner
        self.client.logout()
        self.assertTrue(self.client.login(username=user.username, password=password))
        response = self.client.get(reverse('post_api:post', kwargs={'author_id':author.id, 'post_id':postId}))
        self.assertEqual(response.status_code, 200, f"expected 200. got: {response.status_code}")
        # test admin
        self.client.logout()
        self.auth_helper.authorize_client(self.client)
        response = self.client.get(reverse('post_api:post', kwargs={'author_id':author.id, 'post_id':postId}))
        self.assertEqual(response.status_code, 200, f"expected 200. got: {response.status_code}")

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
        self.assertEqual(response.status_code, 201, f"expected 201. got: {response.status_code}")
        response = self.client.get(reverse('post_api:post', kwargs={'author_id':author.id, 'post_id':"notARealUUID"}))
        self.assertEqual(response.status_code, 404, f"expected 404. got: {response.status_code}")

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
        self.assertEqual(response.status_code, 201, f"expected 201. got: {response.status_code}")
        postId = json.loads(response.content)["data"]["id"].split("posts/")[1].rstrip("/")
        response = self.client.get(reverse('post_api:post', kwargs={'author_id':authorId, 'post_id':postId}))
        self.assertEqual(response.status_code, 404, f"expected 404. got: {response.status_code}")

    def test_get_post_nonexist(self):
        """
        should return 404
        """
        
        author = self.auth_helper.get_author()
        postId = uuid4()
        response = self.client.get(reverse('post_api:post', kwargs={'author_id':author.id, 'post_id':postId}))
        self.assertEqual(response.status_code, 404, f"expected 404. got: {response.status_code}")

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

        response = self.client.put(reverse('post_api:post', kwargs={'author_id':author.id, 'post_id':postId}), oldData, format="json")
        self.assertEqual(response.status_code, 201, f"expected 201. got: {response.status_code}")

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
        
        response = self.client.post(reverse('post_api:post', kwargs={'author_id':author.id, 'post_id':postId}), data, format="json")
        self.assertEqual(response.status_code, 200, f"expected 200. got: {response.status_code}")
        response = self.client.get(reverse('post_api:posts', kwargs={'author_id':author.id}))
        self.assertEqual(response.status_code, 200, f"expected 200. got: {response.status_code}")

        dict_resp = json.loads(response.content)
        self.assertEqual(len(dict_resp["data"]), 1, f"expected list of length 1. got: {len(dict_resp['data'])}")
        dict_resp_data = dict_resp["data"][0]

        self.assertEqual(dict_resp_data["type"], data["type"], "returned item had wrong type!")
        self.assertEqual(dict_resp_data["title"], data["title"], "returned item had wrong title!")
        self.assertEqual(dict_resp_data["description"], data["description"], "returned item had wrong description!")
        self.assertEqual(dict_resp_data["contentType"], data["contentType"], "returned item had wrong contentType!")
        self.assertEqual(dict_resp_data["visibility"], data["visibility"], "returned item had wrong visibility!")
        # Public post uri-id contains its authors id in it
        self.assertIn(str(author.id), dict_resp_data["id"], "returned item referenced wrong author!")

        retPost = Post.objects.get(id=postId)
        self.assertEqual(retPost.title, data["title"], "returned item had wrong title!")
        self.assertEqual(retPost.description, data["description"], "returned item had wrong description!")
        self.assertEqual(str(retPost.contentType), data["contentType"], "returned item had wrong contentType!")
        self.assertEqual(str(retPost.visibility), data["visibility"], "returned item had wrong visibility!")
        # Public post uri-id contains its authors id in it
        self.assertIn(str(author.id), dict_resp_data["id"], "returned item referenced wrong author!")

    def test_post_post_access_levels(self):
        """
        should return 403 for all users except owner
        """

        password = "password"
        user = User.objects.create_user("username1", password=password)
        author: Author = Author.objects.get(userId=user)
        self.client.logout()
        self.client.login(username=user.username, password=password)
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

        response = self.client.put(reverse('post_api:post', kwargs={'author_id':author.id, 'post_id':postId}), oldData, format="json")
        self.assertEqual(response.status_code, 201, f"expected 201. got: {response.status_code}")

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
        
        # test anonymous user
        self.client.logout()
        response = self.client.post(reverse('post_api:post', kwargs={'author_id':author.id, 'post_id':postId}), data, format="json")
        self.assertEqual(response.status_code, 403, f"expected 403. got: {response.status_code}")
        # test non participant
        self.client.logout()
        nonParticipant = User.objects.create_user("nonParticipant", password=password)
        self.assertTrue(self.client.login(username=nonParticipant.username, password=password))
        response = self.client.post(reverse('post_api:post', kwargs={'author_id':author.id, 'post_id':postId}), data, format="json")
        self.assertEqual(response.status_code, 403, f"expected 403. got: {response.status_code}")
        # test owner
        self.client.logout()
        self.assertTrue(self.client.login(username=user.username, password=password))
        response = self.client.post(reverse('post_api:post', kwargs={'author_id':author.id, 'post_id':postId}), data, format="json")
        self.assertEqual(response.status_code, 200, f"expected 200. got: {response.status_code}")
        # test admin
        self.client.logout()
        self.auth_helper.authorize_client(self.client)
        response = self.client.post(reverse('post_api:post', kwargs={'author_id':author.id, 'post_id':postId}), data, format="json")
        self.assertEqual(response.status_code, 403, f"expected 403. got: {response.status_code}")

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
        
        response = self.client.post(reverse('post_api:post', kwargs={'author_id':author.id, 'post_id':postId}), data, format="json")
        self.assertEqual(response.status_code, 404, f"expected 404. got: {response.status_code}")

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
        
        response = self.client.post(reverse('post_api:post', kwargs={'author_id':author.id, 'post_id':postId}), data, format="json")
        self.assertEqual(response.status_code, 404, f"expected 404. got: {response.status_code}")

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

        response = self.client.put(reverse('post_api:post', kwargs={'author_id':author.id, 'post_id':postId}), data, format="json")
        self.assertEqual(response.status_code, 201, f"expected 201. got: {response.status_code}")
        
        response = self.client.post(reverse('post_api:post', kwargs={'author_id':authorId, 'post_id':postId}), data, format="json")
        self.assertEqual(response.status_code, 403, f"expected 403. got: {response.status_code}")

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

        response = self.client.put(reverse('post_api:post', kwargs={'author_id':author.id, 'post_id':postId}), oldData, format="json")
        self.assertEqual(response.status_code, 201, f"expected 201. got: {response.status_code}")

        data = {}
        
        response = self.client.post(reverse('post_api:post', kwargs={'author_id':author.id, 'post_id':postId}), data, format="json")
        self.assertEqual(response.status_code, 200, f"expected 200. got: {response.status_code}")
        response = self.client.get(reverse('post_api:posts', kwargs={'author_id':author.id}))
        self.assertEqual(response.status_code, 200, f"expected 200. got: {response.status_code}")

        dict_resp = json.loads(response.content)
        self.assertEqual(len(dict_resp["data"]), 1, f"expected list of length 1. got: {len(dict_resp['data'])}")
        dict_resp_data = dict_resp["data"][0]

        self.assertEqual(dict_resp_data["type"], oldData["type"], "returned item had wrong type!")
        self.assertEqual(dict_resp_data["title"], oldData["title"], "returned item had wrong title!")
        self.assertEqual(dict_resp_data["description"], oldData["description"], "returned item had wrong description!")
        self.assertEqual(dict_resp_data["contentType"], oldData["contentType"], "returned item had wrong contentType!")
        self.assertEqual(dict_resp_data["visibility"], oldData["visibility"], "returned item had wrong visibility!")
        # Public post uri-id contains its authors id in it
        self.assertIn(str(author.id), dict_resp_data["id"], "returned item referenced wrong author!")

        retPost = Post.objects.get(id=postId)
        self.assertEqual(retPost.title, oldData["title"], "returned item had wrong title!")
        self.assertEqual(retPost.description, oldData["description"], "returned item had wrong description!")
        self.assertEqual(str(retPost.contentType), oldData["contentType"], "returned item had wrong contentType!")
        self.assertEqual(str(retPost.visibility), oldData["visibility"], "returned item had wrong visibility!")
        # Public post uri-id contains its authors id in it
        self.assertIn(str(author.id), dict_resp_data["id"], "returned item referenced wrong author!")

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

        response = self.client.put(reverse('post_api:post', kwargs={'author_id':author.id, 'post_id':postId}), oldData, format="json")
        self.assertEqual(response.status_code, 201, f"expected 201. got: {response.status_code}")

        data = {
            "type":"someOtherType",
            "author":{
                "type":"someOtherType",
                "id":"someOtherId"
            },
        }
        
        response = self.client.post(reverse('post_api:post', kwargs={'author_id':author.id, 'post_id':postId}), data, format="json")
        self.assertEqual(response.status_code, 200, f"expected 200. got: {response.status_code}")
        response = self.client.get(reverse('post_api:posts', kwargs={'author_id':author.id}))
        self.assertEqual(response.status_code, 200, f"expected 200. got: {response.status_code}")

        dict_resp = json.loads(response.content)
        self.assertEqual(len(dict_resp["data"]), 1, f"expected list of length 1. got: {len(dict_resp['data'])}")
        dict_resp_data = dict_resp["data"][0]

        self.assertEqual(dict_resp_data["type"], oldData["type"], "returned item had wrong type!")
        self.assertEqual(dict_resp_data["title"], oldData["title"], "returned item had wrong title!")
        self.assertEqual(dict_resp_data["description"], oldData["description"], "returned item had wrong description!")
        self.assertEqual(dict_resp_data["contentType"], oldData["contentType"], "returned item had wrong contentType!")
        self.assertEqual(dict_resp_data["visibility"], oldData["visibility"], "returned item had wrong visibility!")
        # Public post uri-id contains its authors id in it
        self.assertIn(str(author.id), dict_resp_data["id"], "returned item referenced wrong author!")
        self.assertEqual(dict_resp_data["author"]["type"], "author", "returned item does not have an author object!")

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

        response = self.client.get(reverse('post_api:post', kwargs={'author_id':author.id, 'post_id':postId}))
        self.assertEqual(response.status_code, 200, f"expected 200. got: {response.status_code}")
        response = self.client.delete(reverse('post_api:post', kwargs={'author_id':author.id, 'post_id':postId}))
        self.assertEqual(response.status_code, 204, f"expected 204. got: {response.status_code}")
        response = self.client.get(reverse('post_api:post', kwargs={'author_id':author.id, 'post_id':postId}))
        self.assertEqual(response.status_code, 404, f"expected 404. got: {response.status_code}")

    def test_delete_post_access_levels(self):
        """
        should return 403 for all users except owner
        """

        password = "password"
        user = User.objects.create_user("username1", password=password)
        author: Author = Author.objects.get(userId=user)
        self.client.logout()
        self.client.login(username=user.username, password=password)
        title = "TITLE"
        description = "DESC"
        contentType = Post.ContentTypeEnum.PLAIN
        visibility = Post.VisibilityEnum.PUBLIC
        post = Post.objects.create(title=title, description=description, contentType=contentType, visibility=visibility, author=author)
        post.save()

        postId = post.id

        response = self.client.get(reverse('post_api:post', kwargs={'author_id':author.id, 'post_id':postId}))
        self.assertEqual(response.status_code, 200, f"expected 200. got: {response.status_code}")
        
        # test anonymous user
        self.client.logout()
        response = self.client.delete(reverse('post_api:post', kwargs={'author_id':author.id, 'post_id':postId}))
        self.assertEqual(response.status_code, 403, f"expected 403. got: {response.status_code}")
        # test non participant
        self.client.logout()
        nonParticipant = User.objects.create_user("nonParticipant", password=password)
        self.assertTrue(self.client.login(username=nonParticipant.username, password=password))
        response = self.client.delete(reverse('post_api:post', kwargs={'author_id':author.id, 'post_id':postId}))
        self.assertEqual(response.status_code, 403, f"expected 403. got: {response.status_code}")
        # test owner
        self.client.logout()
        self.assertTrue(self.client.login(username=user.username, password=password))
        response = self.client.delete(reverse('post_api:post', kwargs={'author_id':author.id, 'post_id':postId}))
        self.assertEqual(response.status_code, 204, f"expected 204. got: {response.status_code}")
        # need to recreate for future tests
        post = Post.objects.create(title=title, description=description, contentType=contentType, visibility=visibility, author=author)
        post.save()
        postId = post.id
        response = self.client.get(reverse('post_api:post', kwargs={'author_id':author.id, 'post_id':postId}))
        self.assertEqual(response.status_code, 200, f"expected 200. got: {response.status_code}")
        # test admin
        self.client.logout()
        self.auth_helper.authorize_client(self.client)
        response = self.client.delete(reverse('post_api:post', kwargs={'author_id':author.id, 'post_id':postId}))
        self.assertEqual(response.status_code, 403, f"expected 403. got: {response.status_code}")

    def test_delete_post_nonexist(self):
        """
        should return 404
        """
        
        author = self.auth_helper.get_author()
        postId = uuid4()
        response = self.client.delete(reverse('post_api:post', kwargs={'author_id':author.id, 'post_id':postId}), format="json")
        self.assertEqual(response.status_code, 404, f"expected 404. got: {response.status_code}")

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

        response = self.client.put(reverse('post_api:post', kwargs={'author_id':author.id, 'post_id':postId}), data, format="json")
        self.assertEqual(response.status_code, 201, f"expected 201. got: {response.status_code}")

        authorId = uuid4()
        
        response = self.client.delete(reverse('post_api:post', kwargs={'author_id':authorId, 'post_id':postId}), format="json")
        self.assertEqual(response.status_code, 403, f"expected 403. got: {response.status_code}")

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
        self.assertEqual(response.status_code, 201, f"expected 201. got: {response.status_code}")
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
        self.assertEqual(response.status_code, 201, f"expected 201. got: {response.status_code}")
        dict_resp_data = json.loads(response.content)["data"]
        self.assertEqual(dict_resp_data["type"], comment_data["type"], "returned item had wrong type!")
        self.assertEqual(dict_resp_data["comment"], comment_data["comment"], "returned item had wrong comment!")
        self.assertEqual(dict_resp_data["contentType"], comment_data["contentType"], "returned item had wrong contentType!")
        self.assertEqual(dict_resp_data["author"]["id"], str(author.id), "returned item referenced wrong author!")

    def test_post_comment_access_levels(self):
        """
        should return 403 for all users except ownere
        """
        
        password = "password"
        user = User.objects.create_user("username1", password=password)
        author: Author = Author.objects.get(userId=user)
        self.client.logout()
        self.client.login(username=user.username, password=password)

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
        self.assertEqual(response.status_code, 201, f"expected 201. got: {response.status_code}")
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

        # test anonymous user
        self.client.logout()
        response = self.client.post(reverse('post_api:comments', kwargs={'author_id':author.id, 'post_id':postId}), comment_data, format="json")
        self.assertEqual(response.status_code, 403, f"expected 403. got: {response.status_code}")
        # test non participant
        self.client.logout()
        nonParticipant = User.objects.create_user("nonParticipant", password=password)
        self.assertTrue(self.client.login(username=nonParticipant.username, password=password))
        response = self.client.post(reverse('post_api:comments', kwargs={'author_id':author.id, 'post_id':postId}), comment_data, format="json")
        # everyone should be able to comment, as long as we add friend/private permissions ~~~
        self.assertEqual(response.status_code, 201, f"expected 201. got: {response.status_code}")
        # test owner
        self.client.logout()
        self.assertTrue(self.client.login(username=user.username, password=password))
        response = self.client.post(reverse('post_api:comments', kwargs={'author_id':author.id, 'post_id':postId}), comment_data, format="json")
        self.assertEqual(response.status_code, 201, f"expected 201. got: {response.status_code}")
        # test admin
        self.client.logout()
        self.auth_helper.authorize_client(self.client)
        response = self.client.post(reverse('post_api:comments', kwargs={'author_id':author.id, 'post_id':postId}), comment_data, format="json")
        self.assertEqual(response.status_code, 201, f"expected 201. got: {response.status_code}")

    def test_post_comment_no_data(self):
        """
        should not create a comment since the author of the comment is unknown
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
        self.assertEqual(response.status_code, 201, f"expected 201. got: {response.status_code}")
        postId = json.loads(response.content)["data"]["id"].split("posts/")[1].rstrip("/")

        comment_data = {}

        response = self.client.post(reverse('post_api:comments', kwargs={'author_id':author.id, 'post_id':postId}), comment_data, format="json")
        self.assertEqual(response.status_code, 400, f"expected 400. got: {response.status_code}")

        response = self.client.get(reverse('post_api:comments', kwargs={'author_id':author.id, 'post_id':postId}))
        self.assertEqual(response.status_code, 200, f"expected 200. got: {response.status_code}")

        dict_resp_data = json.loads(response.content)["data"]
        self.assertEquals(len(dict_resp_data), 0, f"expected list of length 0. got: {len(dict_resp_data)}")

    def test_post_comment_min_data(self):
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
        self.assertEqual(response.status_code, 201, f"expected 201. got: {response.status_code}")
        postId = json.loads(response.content)["data"]["id"].split("posts/")[1].rstrip("/")

        comment_data = {
            "author":{
                "type":"author",
                "id":f"{author.id}"
            },
        }

        response = self.client.post(reverse('post_api:comments', kwargs={'author_id':author.id, 'post_id':postId}), comment_data, format="json")
        self.assertEqual(response.status_code, 201, f"expected 201. got: {response.status_code}")

        response = self.client.get(reverse('post_api:comments', kwargs={'author_id':author.id, 'post_id':postId}))
        self.assertEqual(response.status_code, 200, f"expected 200. got: {response.status_code}")

        dict_resp_data = json.loads(response.content)["data"]
        self.assertEquals(len(dict_resp_data), 1, f"expected list of length 1. got: {len(dict_resp_data)}")

        data = dict_resp_data[0]
        self.assertEqual(data["type"], "comment", "returned item had wrong type!")
        self.assertEqual(data["comment"], "", "returned item had wrong comment!")
        self.assertEqual(data["contentType"], f"{Comment.ContentTypeEnum.PLAIN}", "returned item had wrong contentType!")
        self.assertEqual(data["author"]["id"], str(author.id), "returned item referenced wrong author!")

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
        self.assertEqual(response.status_code, 201, f"expected 201. got: {response.status_code}")
        postId = json.loads(response.content)["data"]["id"].split("posts/")[1].rstrip("/")

        comment_data = {
            "type":"someOtherType",
            "author":{
                "type":"someOtherType",
                "id":f"{author.id}"
            },
            "comment":"A Comment with words and markdown",
            "contentType":f"{Comment.ContentTypeEnum.MARKDOWN}"
        }

        response = self.client.post(reverse('post_api:comments', kwargs={'author_id':author.id, 'post_id':postId}), comment_data, format="json")
        self.assertEqual(response.status_code, 201, f"expected 201. got: {response.status_code}")

        response = self.client.get(reverse('post_api:comments', kwargs={'author_id':author.id, 'post_id':postId}))
        self.assertEqual(response.status_code, 200, f"expected 200. got: {response.status_code}")

        dict_resp_data = json.loads(response.content)["data"]
        self.assertEquals(len(dict_resp_data), 1, f"expected list of length 1. got: {len(dict_resp_data)}")

        data = dict_resp_data[0]
        self.assertEqual(data["type"], "comment", "returned item had wrong type!")
        self.assertEqual(data["comment"], comment_data["comment"], "returned item had wrong comment!")
        self.assertEqual(data["contentType"], comment_data["contentType"], "returned item had wrong contentType!")
        self.assertEqual(data["author"]["id"], str(author.id), "returned item referenced wrong type!")
        self.assertEqual(data["author"]["type"], "author", "returned item modified author type!")

    # GETs #####################

    def test_get_comments_no_posts(self):
        """
        should return an empty list
        """
        
        author = self.auth_helper.get_author()
        postId = uuid4()
        response = self.client.get(reverse('post_api:comments', kwargs={'author_id':author.id, 'post_id':postId}))
        self.assertEqual(response.status_code, 200, f"expected 200. got: {response.status_code}")
        self.assertEquals(len(json.loads(response.content)["data"]), 0, "list should have been empty but wasn't!")

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
        self.assertEqual(response.status_code, 201, f"expected 201. got: {response.status_code}")
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
        self.assertEqual(response.status_code, 201, f"expected 201. got: {response.status_code}")
        response = self.client.post(reverse('post_api:comments', kwargs={'author_id':author.id, 'post_id':postId}), comment_data2, format="json")
        self.assertEqual(response.status_code, 201, f"expected 201. got: {response.status_code}")
        response = self.client.get(reverse('post_api:comments', kwargs={'author_id':author.id, 'post_id':postId}))
        self.assertEqual(response.status_code, 200, f"expected 200. got: {response.status_code}")

        dict_resp_data = json.loads(response.content)["data"]
        self.assertEquals(len(dict_resp_data), 2)

        data1 = dict_resp_data[0]
        data2 = dict_resp_data[1]

        if(data1["comment"] != comment_data["comment"]):
            temp = data2
            data2 = data1
            data1 = temp
        
        self.assertEqual(data1["type"], comment_data["type"], "returned item had wrong type!")
        self.assertEqual(data1["comment"], comment_data["comment"], "returned item had wrong comment!")
        self.assertEqual(data1["contentType"], comment_data["contentType"], "returned item had wrong contentType!")
        self.assertEqual(data1["author"]["id"], str(author.id), "returned item referenced wrong author!")

        self.assertEqual(data2["type"], comment_data2["type"], "returned item had wrong type!")
        self.assertEqual(data2["comment"], comment_data2["comment"], "returned item had wrong comment!")
        self.assertEqual(data2["contentType"], comment_data2["contentType"], "returned item had wrong contentType!")
        self.assertEqual(data2["author"]["id"], str(author.id), "returned item referenced wrong author!")

    def test_get_comments_access_levels(self):
        """
        should return 200 for all users
        """
        
        password = "password"
        user = User.objects.create_user("username1", password=password)
        author: Author = Author.objects.get(userId=user)
        self.client.logout()
        self.client.login(username=user.username, password=password)

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
        self.assertEqual(response.status_code, 201, f"expected 201. got: {response.status_code}")
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
        self.assertEqual(response.status_code, 201, f"expected 201. got: {response.status_code}")
        response = self.client.post(reverse('post_api:comments', kwargs={'author_id':author.id, 'post_id':postId}), comment_data2, format="json")
        self.assertEqual(response.status_code, 201, f"expected 201. got: {response.status_code}")
        
        response = self.client.get(reverse('post_api:comments', kwargs={'author_id':author.id, 'post_id':postId}))
        self.assertEqual(response.status_code, 200, f"expected 200. got: {response.status_code}")
        # test anonymous user
        self.client.logout()
        response = self.client.get(reverse('post_api:comments', kwargs={'author_id':author.id, 'post_id':postId}))
        self.assertEqual(response.status_code, 200, f"expected 200. got: {response.status_code}")
        # test non participant
        self.client.logout()
        nonParticipant = User.objects.create_user("nonParticipant", password=password)
        self.assertTrue(self.client.login(username=nonParticipant.username, password=password))
        response = self.client.get(reverse('post_api:comments', kwargs={'author_id':author.id, 'post_id':postId}))
        self.assertEqual(response.status_code, 200, f"expected 200. got: {response.status_code}")
        # test owner
        self.client.logout()
        self.assertTrue(self.client.login(username=user.username, password=password))
        response = self.client.get(reverse('post_api:comments', kwargs={'author_id':author.id, 'post_id':postId}))
        self.assertEqual(response.status_code, 200, f"expected 200. got: {response.status_code}")
        # test admin
        self.client.logout()
        self.auth_helper.authorize_client(self.client)
        response = self.client.get(reverse('post_api:comments', kwargs={'author_id':author.id, 'post_id':postId}))
        self.assertEqual(response.status_code, 200, f"expected 200. got: {response.status_code}")

    def test_get_comments_author_nonexist(self):
        """
        should return 403
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
        self.assertEqual(response.status_code, 201, f"expected 201. got: {response.status_code}")
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
        self.assertEqual(response.status_code, 404, f"expected 404. got: {response.status_code}")

    def test_get_comments_bad_uuid(self):
        """
        should return 403
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
        self.assertEqual(response.status_code, 201, f"expected 201. got: {response.status_code}")
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
        self.assertEqual(response.status_code, 404, f"expected 404. got: {response.status_code}")
