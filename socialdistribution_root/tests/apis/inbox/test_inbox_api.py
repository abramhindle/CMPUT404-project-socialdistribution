from django.test import TestCase
from django.urls import reverse
import json

from rest_framework.test import APIClient

from tests.test_helper.auth_helper import AuthHelper

from socialdistribution.pagination import DEFAULT_PAGE
from socialdistribution.pagination import DEFAULT_PAGE_SIZE

from apps.inbox.models import InboxItem
from apps.posts.models import Post, Comment

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
        self.assertEqual(response.status_code, 201)
        post_data = json.loads(response.content)["data"]
        
        response = self.client.post(reverse('inbox:inbox', kwargs={'author_id':author.id}), post_data, format="json")
        self.assertEqual(response.status_code, 201)
        dict_resp_data = json.loads(response.content)["data"]

        self.assertEqual(dict_resp_data["type"], post_data["type"])
        self.assertEqual(dict_resp_data["title"], post_data["title"])
        self.assertEqual(dict_resp_data["description"], post_data["description"])
        self.assertEqual(dict_resp_data["contentType"], post_data["contentType"])
        self.assertEqual(dict_resp_data["visibility"], post_data["visibility"])
        # Public post uri-id contains its authors id in it
        self.assertIn(str(author.id), dict_resp_data["id"])
        postId = dict_resp_data["id"].split("posts/")[1].rstrip("/")

        # TODO: do this same test on likes

        response = self.client.get(reverse('inbox:inbox', kwargs={'author_id':author.id}))
        self.assertEqual(response.status_code, 200)
        returned_list = json.loads(response.content)["data"]

        self.assertEqual(len(returned_list), 1)

        data1 = returned_list[0]
        self.assertEqual(data1["type"], post_data["type"])
        self.assertEqual(data1["title"], post_data["title"])
        self.assertEqual(data1["description"], post_data["description"])
        self.assertEqual(data1["contentType"], post_data["contentType"])
        self.assertEqual(data1["visibility"], post_data["visibility"])
        # Public post uri-id contains its authors id in it
        self.assertIn(str(author.id), data1["id"])

    def test_get_inbox_author_nonexist(self):
            """
            should return 404
            """
            authorId = uuid4()
            response = self.client.get(reverse('inbox:inbox', kwargs={'author_id':authorId}))
            self.assertEqual(response.status_code, 404)

    def test_get_inbox_bad_uuid(self):
        """
        should return 404
        """
        authorId = "notARealUUID"
        response = self.client.get(reverse('inbox:inbox', kwargs={'author_id':authorId}))
        self.assertEqual(response.status_code, 404)

    def test_get_inbox_empty(self):
        """
        should return 200 with no data except pagination
        """

        author = self.auth_helper.get_author()
        response = self.client.get(reverse('inbox:inbox', kwargs={'author_id':author.id}))

        self.assertEqual(response.status_code, 200)
        dict_resp = json.loads(response.content)

        # checking default pagination
        self.assertEqual(dict_resp["page"], DEFAULT_PAGE)
        self.assertEqual(dict_resp["size"], DEFAULT_PAGE_SIZE)

        self.assertEqual(len(dict_resp["data"]), 0)

    # POSTs ####################

    # TODO: test_post_inbox_original_not_in_db (not supported yet)
    #       test_post_inbox_swapped_type
    #       validate that inbox items actually exist

    # TODO: test with friend requests once implemented
    def test_post_inbox(self):
        """
        should return the created items 
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
        self.assertEqual(response.status_code, 201)
        post_data = json.loads(response.content)["data"]
        
        response = self.client.post(reverse('inbox:inbox', kwargs={'author_id':author.id}), post_data, format="json")
        self.assertEqual(response.status_code, 201)
        dict_resp_data = json.loads(response.content)["data"]

        self.assertEqual(dict_resp_data["type"], post_data["type"])
        self.assertEqual(dict_resp_data["title"], post_data["title"])
        self.assertEqual(dict_resp_data["description"], post_data["description"])
        self.assertEqual(dict_resp_data["contentType"], post_data["contentType"])
        self.assertEqual(dict_resp_data["visibility"], post_data["visibility"])
        # Public post uri-id contains its authors id in it
        self.assertIn(str(author.id), dict_resp_data["id"])
        postId = dict_resp_data["id"].split("posts/")[1].rstrip("/")

        # TODO: do this same test on likes

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
        self.assertEqual(response.status_code, 201)
        post_data = json.loads(response.content)["data"]
        
        response = self.client.post(reverse('inbox:inbox', kwargs={'author_id':author.id}), post_data, format="json")
        self.assertEqual(response.status_code, 201)
        dict_resp_data = json.loads(response.content)["data"]

        self.assertEqual(dict_resp_data["type"], post_data["type"])
        self.assertEqual(dict_resp_data["title"], post_data["title"])
        self.assertEqual(dict_resp_data["description"], post_data["description"])
        self.assertEqual(dict_resp_data["contentType"], post_data["contentType"])
        self.assertEqual(dict_resp_data["visibility"], post_data["visibility"])
        # Public post uri-id contains its authors id in it
        self.assertIn(str(author.id), dict_resp_data["id"])
        postId = dict_resp_data["id"].split("posts/")[1].rstrip("/")

        # TODO: do this same test on likes

        post_data["title"] = "A different title"
        post_data["description"] = "A different description"
        post_data["contentType"] = f"{Post.ContentTypeEnum.PLAIN}"
        post_data["tivisibilitytle"] = f"{Post.VisibilityEnum.FRIENDS}"

        response = self.client.post(reverse('inbox:inbox', kwargs={'author_id':author.id}), post_data, format="json")
        self.assertEqual(response.status_code, 201)
        dict_resp_data = json.loads(response.content)["data"]

        self.assertEqual(dict_resp_data["type"], post_data["type"])
        self.assertEqual(dict_resp_data["title"], post_data["title"])
        self.assertEqual(dict_resp_data["description"], post_data["description"])
        self.assertEqual(dict_resp_data["contentType"], post_data["contentType"])
        self.assertEqual(dict_resp_data["visibility"], post_data["visibility"])
        # Public post uri-id contains its authors id in it
        self.assertIn(str(author.id), dict_resp_data["id"])

        response = self.client.get(reverse('inbox:inbox', kwargs={'author_id':author.id}))
        self.assertEqual(response.status_code, 200)
        returned_list = json.loads(response.content)["data"]

        self.assertEqual(len(returned_list), 1)

        data1 = returned_list[0]
        self.assertEqual(data1["type"], post_data["type"])
        self.assertEqual(data1["title"], post_data["title"])
        self.assertEqual(data1["description"], post_data["description"])
        self.assertEqual(data1["contentType"], post_data["contentType"])
        self.assertEqual(data1["visibility"], post_data["visibility"])
        # Public post uri-id contains its authors id in it
        self.assertIn(str(author.id), data1["id"])

    def test_post_inbox_no_data(self):
        """
        should return 400
        """

        author = self.auth_helper.get_author()
        data = {}

        # need to do this because inbox expects an id
        response = self.client.post(reverse('inbox:inbox', kwargs={'author_id':author.id}), data, format="json")
        self.assertEqual(response.status_code, 400)

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
        self.assertEqual(response.status_code, 201)
        post_data = json.loads(response.content)["data"]
        
        post_data["type"] = "someOtherType"

        response = self.client.post(reverse('inbox:inbox', kwargs={'author_id':author.id}), post_data, format="json")
        self.assertEqual(response.status_code, 400)

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
        self.assertEqual(response.status_code, 201)
        post_data = json.loads(response.content)["data"]

        authorId = uuid4()

        response = self.client.post(reverse('inbox:inbox', kwargs={'author_id':authorId}), post_data, format="json")
        self.assertEqual(response.status_code, 404)

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
        self.assertEqual(response.status_code, 201)
        post_data = json.loads(response.content)["data"]

        authorId = "notARealUUID"

        response = self.client.post(reverse('inbox:inbox', kwargs={'author_id':authorId}), post_data, format="json")
        self.assertEqual(response.status_code, 404)

    # DELETEs ##################

    def test_delete_inbox(self):
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
        self.assertEqual(response.status_code, 201)
        post_data = json.loads(response.content)["data"]
        
        response = self.client.post(reverse('inbox:inbox', kwargs={'author_id':author.id}), post_data, format="json")
        self.assertEqual(response.status_code, 201)

        response = self.client.delete(reverse('inbox:inbox', kwargs={'author_id':author.id}))
        self.assertEqual(response.status_code, 200)

        response = self.client.get(reverse('inbox:inbox', kwargs={'author_id':author.id}))

        self.assertEqual(response.status_code, 200)
        dict_resp = json.loads(response.content)

        # checking default pagination
        self.assertEqual(dict_resp["page"], DEFAULT_PAGE)
        self.assertEqual(dict_resp["size"], DEFAULT_PAGE_SIZE)

        self.assertEqual(len(dict_resp["data"]), 0)

    def test_delete_inbox_empty(self):
        """
        should return 404
        """
        
        author = self.auth_helper.get_author()

        response = self.client.delete(reverse('inbox:inbox', kwargs={'author_id':author.id}))
        self.assertEqual(response.status_code, 404)

    def test_delete_inbox_author_nonexist(self):
        """
        should return 404
        """

        authorId = uuid4()

        response = self.client.delete(reverse('inbox:inbox', kwargs={'author_id':authorId}))
        self.assertEqual(response.status_code, 404)

    def test_delete_inbox_bad_uuid(self):
        """
        should return 404
        """

        authorId = "notARealUUID"

        response = self.client.delete(reverse('inbox:inbox', kwargs={'author_id':authorId}))
        self.assertEqual(response.status_code, 404)
