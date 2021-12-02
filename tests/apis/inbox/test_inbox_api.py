from django.test import TestCase
from django.urls import reverse
import json

from rest_framework.test import APIClient

from tests.test_helper.auth_helper import AuthHelper

from socialdistribution.pagination import DEFAULT_PAGE
from socialdistribution.pagination import DEFAULT_PAGE_SIZE

from apps.core.models import Author, User
from apps.inbox.models import InboxItem
from apps.posts.models import Post

from uuid import uuid4

class InboxViewTests(TestCase):
    def setUp(self):
        self.auth_helper = AuthHelper()
        self.auth_helper.setup()
        self.client = APIClient()
        self.auth_helper.authorize_client(self.client)

    # GETs #####################

    # TODO: test with friend requests once implemented
    def test_get_inbox(self):
        """
        should return the created items 
        """

        author = self.auth_helper.get_author()
        user = User(username="username1")
        user.save()
        author2: Author = Author.objects.get(userId=user)
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

        # need to do this because inbox expects an id
        response = self.client.post(reverse('post_api:posts', kwargs={'author_id':author.id}), data, format="json")
        self.assertEqual(response.status_code, 201, f"expected 201. got: {response.status_code}")
        post_data = json.loads(response.content)["data"]
        data["id"] = post_data["id"]
        # print(post_data)
        # print()
        
        response = self.client.post(reverse('inbox_api:inbox', kwargs={'author_id':author.id}), data, format="json")
        # print(json.loads(response.content))
        self.assertEqual(response.status_code, 201, f"expected 201. got: {response.status_code}")
        dict_resp_data = json.loads(response.content)["data"]

        self.assertEqual(dict_resp_data["type"], data["type"], "returned item had wrong type!")
        self.assertEqual(dict_resp_data["title"], data["title"], "returned item had wrong title!")
        self.assertEqual(dict_resp_data["description"], data["description"], "returned item had wrong description!")
        self.assertEqual(dict_resp_data["contentType"], data["contentType"], "returned item had wrong contentType!")
        self.assertEqual(dict_resp_data["visibility"], data["visibility"], "returned item had wrong visibility!")
        # Public post uri-id contains its authors id in it
        self.assertIn(str(author.id), dict_resp_data["id"], "returned item referenced wrong author!")
        postId = dict_resp_data["id"]

        data = {
            "object": f"{postId}",
            "author":{
                "type":"author",
                "id":f"{author2.id}"
            },
        }

        response = self.client.post(reverse('likes_api:inbox_like', kwargs={'author_id':author.id}), data, format="json")
        self.assertEqual(response.status_code, 201, f"expected 201. got: {response.status_code}")
        like_data = json.loads(response.content)["data"]
        
        self.assertEqual(postId, like_data["object"], "returned item referenced wrong object!")
        self.assertEqual(like_data["author"]["id"], str(author2.id), "returned item referenced wrong author!")

        response = self.client.post(reverse('inbox_api:inbox', kwargs={'author_id':author.id}), like_data, format="json")
        self.assertEqual(response.status_code, 201, f"expected 201. got: {response.status_code}")
        dict_resp_data = json.loads(response.content)["data"]

        response = self.client.get(reverse('inbox_api:inbox', kwargs={'author_id':author.id}))
        self.assertEqual(response.status_code, 200, f"expected 200. got: {response.status_code}")
        returned_list = json.loads(response.content)["data"]

        self.assertEqual(len(returned_list), 2, f"expected 2 items. got: {len(returned_list)}")

        data1 = returned_list[0]
        data2 = returned_list[1]
        if "object" in data1:
            temp = data1
            data1 = data2
            data2 = temp
        self.assertEqual(data1["type"], post_data["type"], "returned item had wrong type!")
        self.assertEqual(data1["title"], post_data["title"], "returned item had wrong title!")
        self.assertEqual(data1["description"], post_data["description"], "returned item had wrong description!")
        self.assertEqual(data1["contentType"], post_data["contentType"], "returned item had wrong contentType!")
        self.assertEqual(data1["visibility"], post_data["visibility"], "returned item had wrong visibility!")
        # Public post uri-id contains its authors id in it
        self.assertIn(str(author.id), data1["id"], "returned item referenced wrong author!")

        self.assertEqual(data2["object"], postId, "returned item referenced wrong object!")
        self.assertEqual(data2["author"]["id"], str(author2.id), "returned item referenced wrong author!")

    def test_get_inbox_access_levels(self):
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

        # need to do this because inbox expects an id
        # author creates a post
        response = self.client.post(reverse('post_api:posts', kwargs={'author_id':author.id}), data, format="json")
        self.assertEqual(response.status_code, 201, f"expected 201. got: {response.status_code}")
        post_data = json.loads(response.content)["data"]
        data["id"] = post_data["id"]
        
        # author's post gets sent to their inbox
        response = self.client.post(reverse('inbox_api:inbox', kwargs={'author_id':author.id}), data, format="json")
        self.assertEqual(response.status_code, 201, f"expected 201. got: {response.status_code}")
        # test admin
        self.client.logout()
        self.auth_helper.authorize_client(self.client)
        response = self.client.post(reverse('inbox_api:inbox', kwargs={'author_id':author.id}), data, format="json")
        self.assertEqual(response.status_code, 201, f"expected 201. got: {response.status_code}")

        dict_resp_data = json.loads(response.content)["data"]
        postId = dict_resp_data["id"]

        # author 2 likes author's post
        self.client.logout()
        self.client.login(username=user2.username, password=password)
        data = {
            "object": f"{postId}",
            "author":{
                "type":"author",
                "id":f"{author2.id}"
            },
        }

        response = self.client.post(reverse('likes_api:inbox_like', kwargs={'author_id':author.id}), data, format="json")
        self.assertEqual(response.status_code, 201, f"expected 201. got: {response.status_code}")
        like_data = json.loads(response.content)["data"]
        
        response = self.client.post(reverse('inbox_api:inbox', kwargs={'author_id':author.id}), like_data, format="json")
        self.assertEqual(response.status_code, 201, f"expected 201. got: {response.status_code}")
        dict_resp_data = json.loads(response.content)["data"]

        # test anonymous user
        self.client.logout()
        response = self.client.get(reverse('inbox_api:inbox', kwargs={'author_id':author.id}))
        self.assertEqual(response.status_code, 200, f"expected 200. got: {response.status_code}")
        # test non participant
        self.client.logout()
        nonParticipant = User.objects.create_user("nonParticipant", password=password)
        self.assertTrue(self.client.login(username=nonParticipant.username, password=password))
        response = self.client.get(reverse('inbox_api:inbox', kwargs={'author_id':author.id}))
        self.assertEqual(response.status_code, 200, f"expected 200. got: {response.status_code}")
        # test inbox owner
        self.client.logout()
        self.assertTrue(self.client.login(username=user.username, password=password))
        response = self.client.get(reverse('inbox_api:inbox', kwargs={'author_id':author.id}))
        self.assertEqual(response.status_code, 200, f"expected 200. got: {response.status_code}")

    def test_get_inbox_author_nonexist(self):
            """
            should return 404
            """
            authorId = uuid4()
            response = self.client.get(reverse('inbox_api:inbox', kwargs={'author_id':authorId}))
            self.assertEqual(response.status_code, 404, f"expected 404. got: {response.status_code}")

    def test_get_inbox_bad_uuid(self):
        """
        should return 404
        """
        authorId = "notARealUUID"
        response = self.client.get(reverse('inbox_api:inbox', kwargs={'author_id':authorId}))
        self.assertEqual(response.status_code, 404, f"expected 404. got: {response.status_code}")

    def test_get_inbox_empty(self):
        """
        should return 200 with no data except pagination
        """

        author = self.auth_helper.get_author()
        response = self.client.get(reverse('inbox_api:inbox', kwargs={'author_id':author.id}))

        self.assertEqual(response.status_code, 200, f"expected 200. got: {response.status_code}")
        dict_resp = json.loads(response.content)

        # checking default pagination
        self.assertEqual(dict_resp["page"], DEFAULT_PAGE, f"expected page {DEFAULT_PAGE}. got: {dict_resp['page']}")
        self.assertEqual(dict_resp["size"], DEFAULT_PAGE_SIZE, f"expected page size {DEFAULT_PAGE_SIZE}. got: {dict_resp['size']}")

        self.assertEqual(len(dict_resp["data"]), 0, "inbox should have been empty but wasn't!")

    # POSTs ####################

    # TODO: test_post_inbox_original_nonexist (not supported yet)

    # TODO: test with friend requests once implemented
    def test_post_inbox(self):
        """
        should return the created items 
        """

        author = self.auth_helper.get_author()
        user = User(username="username1")
        user.save()
        author2: Author = Author.objects.get(userId=user)
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

        # need to do this because inbox expects an id
        response = self.client.post(reverse('post_api:posts', kwargs={'author_id':author.id}), data, format="json")
        self.assertEqual(response.status_code, 201, f"expected 201. got: {response.status_code}")
        post_data = json.loads(response.content)["data"]
        data["id"] = post_data["id"]
        
        response = self.client.post(reverse('inbox_api:inbox', kwargs={'author_id':author.id}), data, format="json")
        self.assertEqual(response.status_code, 201, f"expected 201. got: {response.status_code}")
        dict_resp_data = json.loads(response.content)["data"]

        self.assertEqual(dict_resp_data["type"], data["type"], "returned item had wrong type!")
        self.assertEqual(dict_resp_data["title"], data["title"], "returned item had wrong title!")
        self.assertEqual(dict_resp_data["description"], data["description"], "returned item had wrong description!")
        self.assertEqual(dict_resp_data["contentType"], data["contentType"], "returned item had wrong contentType!")
        self.assertEqual(dict_resp_data["visibility"], data["visibility"], "returned item had wrong visibility!")
        # Public post uri-id contains its authors id in it
        self.assertIn(str(author.id), dict_resp_data["id"], "returned item referenced wrong author!")
        postId = dict_resp_data["id"]

        data = {
            "object": f"{postId}",
            "author":{
                "type":"author",
                "id":f"{author2.id}"
            },
        }

        response = self.client.post(reverse('likes_api:inbox_like', kwargs={'author_id':author.id}), data, format="json")
        self.assertEqual(response.status_code, 201, f"expected 201. got: {response.status_code}")
        like_data = json.loads(response.content)["data"]
        
        self.assertEqual(postId, like_data["object"], "returned item referenced wrong object!")
        self.assertEqual(like_data["author"]["id"], str(author2.id), "returned item referenced wrong author!")

        response = self.client.post(reverse('inbox_api:inbox', kwargs={'author_id':author.id}), like_data, format="json")
        self.assertEqual(response.status_code, 201, f"expected 201. got: {response.status_code}")
        dict_resp_data = json.loads(response.content)["data"]

    def test_post_inbox_access_levels(self):
        """
        should return should return 401 for anonymous users, 403 for users who did not own the 
        original content the inbox item references, and 200 for the rightful owner and admins 
        """

        password = "password"
        user = User.objects.create_user("username1", password=password)
        author: Author = Author.objects.get(userId=user)
        user2 = User.objects.create_user("username2", password=password)
        author2: Author = Author.objects.get(userId=user2)
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

        # need to do this because inbox expects an id
        response = self.client.post(reverse('post_api:posts', kwargs={'author_id':author.id}), data, format="json")
        self.assertEqual(response.status_code, 201, f"expected 201. got: {response.status_code}")
        post_data = json.loads(response.content)["data"]
        data["id"] = post_data["id"]

        # author's post gets sent to their inbox
        # test anonymous user
        self.client.logout()
        response = self.client.post(reverse('inbox_api:inbox', kwargs={'author_id':author.id}), data, format="json")
        self.assertEqual(response.status_code, 401, f"expected 401. got: {response.status_code}")
        # test non participant
        self.client.logout()
        self.assertTrue(self.client.login(username=user2.username, password=password))
        response = self.client.post(reverse('inbox_api:inbox', kwargs={'author_id':author.id}), data, format="json")
        self.assertEqual(response.status_code, 403, f"expected 403. got: {response.status_code}")
        # test content owner
        self.client.logout()
        self.assertTrue(self.client.login(username=user.username, password=password))
        response = self.client.post(reverse('inbox_api:inbox', kwargs={'author_id':author.id}), data, format="json")
        self.assertEqual(response.status_code, 201, f"expected 201. got: {response.status_code}")
        response = self.client.post(reverse('inbox_api:inbox', kwargs={'author_id':author2.id}), data, format="json")
        self.assertEqual(response.status_code, 201, f"expected 201. got: {response.status_code}")
        # test admin
        self.client.logout()
        self.auth_helper.authorize_client(self.client)
        response = self.client.post(reverse('inbox_api:inbox', kwargs={'author_id':author.id}), data, format="json")
        self.assertEqual(response.status_code, 201, f"expected 201. got: {response.status_code}")

        dict_resp_data = json.loads(response.content)["data"]
        postId = dict_resp_data["id"]

        self.client.logout()
        self.client.login(username=user2.username, password=password)
        data = {
            "object": f"{postId}",
            "author":{
                "type":"author",
                "id":f"{author2.id}"
            },
        }

        response = self.client.post(reverse('likes_api:inbox_like', kwargs={'author_id':author.id}), data, format="json")
        self.assertEqual(response.status_code, 201, f"expected 201. got: {response.status_code}")
        like_data = json.loads(response.content)["data"]
        
        # test anonymous user
        self.client.logout()
        response = self.client.post(reverse('inbox_api:inbox', kwargs={'author_id':author.id}), like_data, format="json")
        self.assertEqual(response.status_code, 401, f"expected 401. got: {response.status_code}")
        # test non participant
        self.client.logout()
        nonParticipant = User.objects.create_user("nonParticipant", password=password)
        self.assertTrue(self.client.login(username=nonParticipant.username, password=password))
        response = self.client.post(reverse('inbox_api:inbox', kwargs={'author_id':author.id}), like_data, format="json")
        self.assertEqual(response.status_code, 403, f"expected 403. got: {response.status_code}")
        # test likee
        self.client.logout()
        self.assertTrue(self.client.login(username=user.username, password=password))
        response = self.client.post(reverse('inbox_api:inbox', kwargs={'author_id':author.id}), like_data, format="json")
        self.assertEqual(response.status_code, 403, f"expected 403. got: {response.status_code}")
        # test liker
        self.client.logout()
        self.assertTrue(self.client.login(username=user2.username, password=password))
        response = self.client.post(reverse('inbox_api:inbox', kwargs={'author_id':author.id}), like_data, format="json")
        self.assertEqual(response.status_code, 201, f"expected 201. got: {response.status_code}")
        # test admin
        self.client.logout()
        self.auth_helper.authorize_client(self.client)
        response = self.client.post(reverse('inbox_api:inbox', kwargs={'author_id':author.id}), like_data, format="json")
        self.assertEqual(response.status_code, 201, f"expected 201. got: {response.status_code}")


    def test_post_inbox_overwrite(self):
        """
        should return modify the existing entry and not create a new one
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

        # need to do this because inbox expects an id
        response = self.client.post(reverse('post_api:posts', kwargs={'author_id':author.id}), data, format="json")
        self.assertEqual(response.status_code, 201, f"expected 201. got: {response.status_code}")
        post_data = json.loads(response.content)["data"]
        data["id"] = post_data["id"]
        
        response = self.client.post(reverse('inbox_api:inbox', kwargs={'author_id':author.id}), data, format="json")
        self.assertEqual(response.status_code, 201, f"expected 201. got: {response.status_code}")
        dict_resp_data = json.loads(response.content)["data"]

        self.assertEqual(dict_resp_data["type"], data["type"], "returned item had wrong type!")
        self.assertEqual(dict_resp_data["title"], data["title"], "returned item had wrong title!")
        self.assertEqual(dict_resp_data["description"], data["description"], "returned item had wrong description!")
        self.assertEqual(dict_resp_data["contentType"], data["contentType"], "returned item had wrong contentType!")
        self.assertEqual(dict_resp_data["visibility"], data["visibility"], "returned item had wrong visibility!")
        # Public post uri-id contains its authors id in it
        self.assertIn(str(author.id), dict_resp_data["id"], "returned item referenced wrong author!")
        postId = dict_resp_data["id"].split("posts/")[1].rstrip("/")

        data["title"] = "A different title"
        data["description"] = "A different description"
        data["contentType"] = f"{Post.ContentTypeEnum.PLAIN}"
        data["visibility"] = f"{Post.VisibilityEnum.FRIENDS}"

        response = self.client.post(reverse('inbox_api:inbox', kwargs={'author_id':author.id}), data, format="json")
        self.assertEqual(response.status_code, 201, f"expected 201. got: {response.status_code}")
        dict_resp_data = json.loads(response.content)["data"]

        self.assertEqual(dict_resp_data["type"], data["type"], "returned item had wrong type!")
        self.assertEqual(dict_resp_data["title"], data["title"], "returned item had wrong title!")
        self.assertEqual(dict_resp_data["description"], data["description"], "returned item had wrong description!")
        self.assertEqual(dict_resp_data["contentType"], data["contentType"], "returned item had wrong contentType!")
        self.assertEqual(dict_resp_data["visibility"], data["visibility"], "returned item had wrong visibility!")
        # Public post uri-id contains its authors id in it
        self.assertIn(str(author.id), dict_resp_data["id"], "returned item referenced wrong author!")

        response = self.client.get(reverse('inbox_api:inbox', kwargs={'author_id':author.id}))
        self.assertEqual(response.status_code, 200, f"expected 200. got: {response.status_code}")
        returned_list = json.loads(response.content)["data"]

        self.assertEqual(len(returned_list), 1)

        data1 = returned_list[0]
        self.assertEqual(data1["type"], data["type"], "returned item had wrong type!")
        self.assertEqual(data1["title"], data["title"], "returned item had wrong title!")
        self.assertEqual(data1["description"], data["description"], "returned item had wrong description!")
        self.assertEqual(data1["contentType"], data["contentType"], "returned item had wrong contentType!")
        self.assertEqual(data1["visibility"], data["visibility"], "returned item had wrong visibility!")
        # Public post uri-id contains its authors id in it
        self.assertIn(str(author.id), data1["id"], "returned item referenced wrong author!")

    def test_post_inbox_no_data(self):
        """
        should return 400
        """

        author = self.auth_helper.get_author()
        data = {}

        # need to do this because inbox expects an id
        response = self.client.post(reverse('inbox_api:inbox', kwargs={'author_id':author.id}), data, format="json")
        self.assertEqual(response.status_code, 400, f"expected 400. got: {response.status_code}")

    def test_post_inbox_invalid_type(self):
        """
        should return 400
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

        # need to do this because inbox expects an id
        response = self.client.post(reverse('post_api:posts', kwargs={'author_id':author.id}), data, format="json")
        self.assertEqual(response.status_code, 201, f"expected 201. got: {response.status_code}")
        post_data = json.loads(response.content)["data"]
        
        post_data["type"] = "someOtherType"

        response = self.client.post(reverse('inbox_api:inbox', kwargs={'author_id':author.id}), post_data, format="json")
        self.assertEqual(response.status_code, 400, f"expected 400. got: {response.status_code}")

    def test_post_inbox_author_nonexist(self):
        """
        should return 404
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

        # need to do this because inbox expects an id
        response = self.client.post(reverse('post_api:posts', kwargs={'author_id':author.id}), data, format="json")
        self.assertEqual(response.status_code, 201, f"expected 201. got: {response.status_code}")
        post_data = json.loads(response.content)["data"]

        authorId = uuid4()

        response = self.client.post(reverse('inbox_api:inbox', kwargs={'author_id':authorId}), post_data, format="json")
        self.assertEqual(response.status_code, 404, f"expected 404. got: {response.status_code}")

    def test_post_inbox_bad_uuid(self):
        """
        should return 404
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

        # need to do this because inbox expects an id
        response = self.client.post(reverse('post_api:posts', kwargs={'author_id':author.id}), data, format="json")
        self.assertEqual(response.status_code, 201, f"expected 201. got: {response.status_code}")
        post_data = json.loads(response.content)["data"]

        authorId = "notARealUUID"

        response = self.client.post(reverse('inbox_api:inbox', kwargs={'author_id':authorId}), post_data, format="json")
        self.assertEqual(response.status_code, 404, f"expected 404. got: {response.status_code}")

    def test_post_inbox_swapped_type(self):
        """
        should return 400 both times
        """

        author = self.auth_helper.get_author()
        user = User(username="username1")
        user.save()
        author2: Author = Author.objects.get(userId=user)
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

        # need to do this because inbox expects an id
        response = self.client.post(reverse('post_api:posts', kwargs={'author_id':author.id}), data, format="json")
        self.assertEqual(response.status_code, 201, f"expected 201. got: {response.status_code}")
        post_data = json.loads(response.content)["data"]
        postId = post_data["id"]
        data["id"] = post_data["id"]
        data["type"] = f"{InboxItem.ItemTypeEnum.LIKE}"
        
        response = self.client.post(reverse('inbox_api:inbox', kwargs={'author_id':author.id}), data, format="json")
        self.assertEqual(response.status_code, 400, f"expected 400. got: {response.status_code}")

        data = {
            "object": f"{postId}",
            "author":{
                "type":"author",
                "id":f"{author2.id}"
            },
        }

        response = self.client.post(reverse('likes_api:inbox_like', kwargs={'author_id':author.id}), data, format="json")
        self.assertEqual(response.status_code, 201, f"expected 201. got: {response.status_code}")
        like_data = json.loads(response.content)["data"]
        like_data["type"] = "post"
        
        self.assertEqual(postId, like_data["object"], "returned item referenced wrong object!")
        self.assertEqual(like_data["author"]["id"], str(author2.id), "returned item referenced wrong author!")

        response = self.client.post(reverse('inbox_api:inbox', kwargs={'author_id':author.id}), like_data, format="json")
        self.assertEqual(response.status_code, 400, f"expected 400. got: {response.status_code}")

    # DELETEs ##################

    def test_delete_inbox(self):
        """
        should delete the items in the inbox
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

        # need to do this because inbox expects an id
        response = self.client.post(reverse('post_api:posts', kwargs={'author_id':author.id}), data, format="json")
        self.assertEqual(response.status_code, 201, f"expected 201. got: {response.status_code}")
        post_data = json.loads(response.content)["data"]
        data["id"] = post_data["id"]
        
        response = self.client.post(reverse('inbox_api:inbox', kwargs={'author_id':author.id}), data, format="json")
        self.assertEqual(response.status_code, 201, f"expected 201. got: {response.status_code}")

        response = self.client.delete(reverse('inbox_api:inbox', kwargs={'author_id':author.id}))
        self.assertEqual(response.status_code, 204, f"expected 200. got: {response.status_code}")

        response = self.client.get(reverse('inbox_api:inbox', kwargs={'author_id':author.id}))

        self.assertEqual(response.status_code, 200, f"expected 200. got: {response.status_code}")
        dict_resp = json.loads(response.content)

        # checking default pagination
        self.assertEqual(dict_resp["page"], DEFAULT_PAGE, f"expected page {DEFAULT_PAGE}. got: {dict_resp['page']}")
        self.assertEqual(dict_resp["size"], DEFAULT_PAGE_SIZE, f"expected page size {DEFAULT_PAGE_SIZE}. got: {dict_resp['size']}")

        self.assertEqual(len(dict_resp["data"]), 0, "inbox should have been empty but wasn't!")

    def test_delete_inbox_access_levels(self):
        """
        should return 401 for anonymous users, 403 for non owners, 204 for owners and admins
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

        # need to do this because inbox expects an id
        response = self.client.post(reverse('post_api:posts', kwargs={'author_id':author.id}), data, format="json")
        self.assertEqual(response.status_code, 201, f"expected 201. got: {response.status_code}")
        post_data = json.loads(response.content)["data"]
        data["id"] = post_data["id"]
        
        response = self.client.post(reverse('inbox_api:inbox', kwargs={'author_id':author.id}), data, format="json")
        self.assertEqual(response.status_code, 201, f"expected 201. got: {response.status_code}")

        # test anonymous user
        self.client.logout()
        response = self.client.delete(reverse('inbox_api:inbox', kwargs={'author_id':author.id}))
        self.assertEqual(response.status_code, 401, f"expected 401. got: {response.status_code}")
        # test non participant
        self.client.logout()
        nonParticipant = User.objects.create_user("nonParticipant", password=password)
        self.assertTrue(self.client.login(username=nonParticipant.username, password=password))
        response = self.client.delete(reverse('inbox_api:inbox', kwargs={'author_id':author.id}))
        self.assertEqual(response.status_code, 403, f"expected 403. got: {response.status_code}")
        # test owner
        self.client.logout()
        self.assertTrue(self.client.login(username=user.username, password=password))
        response = self.client.delete(reverse('inbox_api:inbox', kwargs={'author_id':author.id}))
        self.assertEqual(response.status_code, 204, f"expected 204. got: {response.status_code}")
        # have to replace for next delete call
        response = self.client.post(reverse('inbox_api:inbox', kwargs={'author_id':author.id}), data, format="json")
        self.assertEqual(response.status_code, 201, f"expected 201. got: {response.status_code}")
        # test admin
        self.client.logout()
        self.auth_helper.authorize_client(self.client)
        response = self.client.delete(reverse('inbox_api:inbox', kwargs={'author_id':author.id}))
        self.assertEqual(response.status_code, 204, f"expected 204. got: {response.status_code}")

    def test_delete_inbox_empty(self):
        """
        should return 404
        """
        
        author = self.auth_helper.get_author()

        response = self.client.delete(reverse('inbox_api:inbox', kwargs={'author_id':author.id}))
        self.assertEqual(response.status_code, 404, f"expected 404. got: {response.status_code}")

    def test_delete_inbox_author_nonexist(self):
        """
        should return 404
        """

        authorId = uuid4()

        response = self.client.delete(reverse('inbox_api:inbox', kwargs={'author_id':authorId}))
        self.assertEqual(response.status_code, 404, f"expected 404. got: {response.status_code}")

    def test_delete_inbox_bad_uuid(self):
        """
        should return 404
        """

        authorId = "notARealUUID"

        response = self.client.delete(reverse('inbox_api:inbox', kwargs={'author_id':authorId}))
        self.assertEqual(response.status_code, 404, f"expected 404. got: {response.status_code}")
