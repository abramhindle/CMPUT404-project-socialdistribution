from django.test import TestCase
from django.urls import reverse
import json

from rest_framework.test import APIClient

from socialdistribution_root.tests.test_helper.auth_helper import AuthHelper

from socialdistribution.pagination import DEFAULT_PAGE
from socialdistribution.pagination import DEFAULT_PAGE_SIZE

class CoreViewTests(TestCase):

    def setup(self):
        self.auth_helper = AuthHelper()
        self.auth_helper.setup()
        self.client = APIClient()
        self.auth_helper.authorize_client(self.client)


    def test_get_posts_empty(self):
        self.setup()
        author = self.auth_helper.get_super_user()
        response = self.client.get(reverse('post_api:posts', kwargs={'author_id':author.id}))

        self.assertEqual(response.status_code, 200)
        dict_resp = json.loads(response.content)

        # checking default pagination
        self.assertEqual(dict_resp["page"], DEFAULT_PAGE)
        self.assertEqual(dict_resp["size"], DEFAULT_PAGE_SIZE)

    def test_post_posts(self):
        self.setup()
        author = self.auth_helper.get_super_user()

        data = {
            "type":"post",
            "title":"A post title about a post about web dev",
            "description":"This post discusses stuff -- brief",
            "contentType":"text/markdown",
            "author":{
                "type":"author",
                "id":"{author.id}"
            },
            "visibility":"PUBLIC",
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
        # Public post uri-id contains it's authors id in it
        self.assertIn(str(author.id), dict_resp_data["id"])