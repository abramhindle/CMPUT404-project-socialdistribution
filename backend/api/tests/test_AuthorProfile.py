from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import RequestsClient
from .util import *
from ..serializers import AuthorProfileSerializer
from ..models import AuthorProfile, Follow
import json
import uuid


class AuthorProfileTestCase(TestCase):
    client = RequestsClient()
    username = "test123"
    password = "pw123"

    username2 = "test123_2"
    password2 = "pw123_2"

    username3 = "test123_3"
    password3 = "pw123_3"

    username4 = "test123_4"
    password4 = "pw123_4"

    expected_output = {
        "host": "http://localhost.com",
        "displayName": "unit test displayname",
        "github": "http://www.github.com/htruong1",
        "bio": "this is a unit test",
        "firstName": "my first name",
        "lastName": "my gucci last name",
        "email": "iloveTDD@TDD.com"
    }

    def setUp(self):
        # create user
        self.user = User.objects.create_user(username=self.username, password=self.password)
        self.user2 = User.objects.create_user(username=self.username2, password=self.password2)
        self.user3 = User.objects.create_user(username=self.username3, password=self.password3)
        self.user4 = User.objects.create_user(username=self.username4, password=self.password4)

        self.authorProfile = AuthorProfile.objects.create(host="http://127.0.0.1:5454/",
                                                          displayName="Lara Croft",
                                                          github="http://github.com/laracroft",
                                                          user=self.user)

        self.authorProfile2 = AuthorProfile.objects.create(host="http://127.0.0.1:5454/",
                                                           displayName="Lara Croft number 2",
                                                           github="http://github.com/laracroft2",
                                                           user=self.user2)

        self.authorProfile3 = AuthorProfile.objects.create(host="http://127.0.0.1:5454/",
                                                           displayName="Lara Croft number 3",
                                                           github="http://github.com/laracroft3",
                                                           user=self.user3)

        self.authorProfile4 = AuthorProfile.objects.create(host="http://127.0.0.1:5454/",
                                                           displayName="Lara Croft number 4",
                                                           github="http://github.com/laracroft4",
                                                           user=self.user4)

        self.user_id = get_author_id(self.authorProfile.host, self.authorProfile.id, False)
        self.user_id2 = get_author_id(self.authorProfile2.host, self.authorProfile2.id, False)
        self.user_id3 = get_author_id(self.authorProfile3.host, self.authorProfile3.id, False)
        self.user_id4 = get_author_id(self.authorProfile4.host, self.authorProfile4.id, False)

        self.user_id_escaped = get_author_id(self.authorProfile.host, self.authorProfile.id, True)

        Follow.objects.create(authorA=self.user_id,
                              authorB=self.user_id2,
                              status="FRIENDS")

        Follow.objects.create(authorA=self.user_id,
                              authorB=self.user_id3,
                              status="FOLLOWING")

        Follow.objects.create(authorA=self.user_id,
                              authorB=self.user_id4,
                              status="FRIENDS")
        
    
    def test_get_author_profile(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.get("/api/author/{}".format(self.authorProfile.id))
        print(response.data)
        self.assertEqual(True, False)

    # def test_get_author_with_invalid_id(self):
    #     self.client.login(username=self.username, password=self.password)
    #     fake_uuid = uuid.uuid4()
    #     response = self.client.get("/api/author/{}".format(fake_uuid))
    #     self.assertEqual(response.status_code, 400)

    # def test_get_valid_id_with_no_auth(self):
    #     response = self.client.get("/api/author/{}".format(self.authorProfile.id))
    #     self.assertEqual(response.status_code, 403)

    # def assert_author_profile(self, expected, output):
    #     for key in expected.keys():
    #         self.assertEqual(expected[key], output[key])

    # def test_get_author_profile_with_auth(self):
    #     self.client.login(username=self.username, password=self.password)
    #     response = self.client.get("/api/author/{}".format(self.authorProfile.id))
    #     self.assertEqual(response.status_code, 200)
    #     self.assert_author_profile(self.expected_output, response.data)

    # def test_invalid_methods(self):
    #     self.client.login(username=self.username, password=self.password)

    #     response = self.client.put("/api/author/{}".format(self.authorProfile.id))
    #     self.assertEqual(response.status_code, 405)
    #     response = self.client.delete("/api/author/{}".format(self.authorProfile.id))
    #     self.assertEqual(response.status_code, 405)
    #     self.client.logout()

    # def test_no_id(self):
    #     self.client.login(username=self.username, password=self.password)
    #     response = self.client.get("/api/author/")
    #     self.assertEqual(response.status_code, 400)

    # def test_no_id_for_post(self):
    #     self.client.login(username=self.username, password=self.password)
    #     response = self.client.post("/api/author/")
    #     self.assertEqual(response.status_code, 400)
    #     self.assertEqual(json.loads(response.content), "Error: Author ID required!")

    # def test_post_update_author(self):
    #     self.client.login(username=self.username, password=self.password)

    #     updated_profile = {
    #         "displayName": "updating display name",
    #         "github": "http://www.github.com/updated_in_test",
    #         "bio": "updating bio",
    #         "firstName": "updating first name",
    #         "lastName": "updating last name",
    #         "email": "TDD4lyfe@unittest.com"
    #     }

    #     expected_profile = {
    #         'id': 'http://localhost.com/author/{}'.format(self.authorProfile.id), 
    #         'host': 'http://localhost.com', 
    #         'displayName': 'updating display name', 
    #         'url': 'http://localhost.com/author/{}'.format(self.authorProfile.id), 
    #         'github': 'http://www.github.com/updated_in_test', 
    #         'firstName': 'updating first name', 
    #         'lastName': 'updating last name', 
    #         'email': 'TDD4lyfe@unittest.com', 
    #         'bio': 'updating bio',
    #         'isValid': False}

    #     response = self.client.post("/api/author/{}".format(self.authorProfile.id), 
    #             data=updated_profile, content_type="application/json")

    #     self.assertEqual(response.status_code, 200)

    #     response = self.client.get("/api/author/{}".format(self.authorProfile.id))
    #     updated_author = json.loads(response.content)
    #     self.assertEqual(updated_author, expected_profile)

    # def test_post_invalid_key(self):
    #     self.client.login(username=self.username, password=self.password)

    #     incorrect_profile_field = {
    #         'id': "fake id",
    #         "host": "http://fakehost.com" 
    #     }

    #     response = self.client.post("/api/author/{}".format(self.authorProfile.id), 
    #         data=incorrect_profile_field, content_type="application/json")

    #     self.assertEqual(response.status_code, 400)
    #     self.assertEqual(json.loads(response.content), "Error: Can't modify field")

    # #trying to update an author but it doesn't exist
    # def test_post_non_existant_id(self):
    #     self.client.login(username=self.username, password=self.password)

    #     updated_profile = {
    #         "displayName": "updating display name",
    #         "github": "http://www.github.com/updated_in_test",
    #         "bio": "updating bio",
    #         "firstName": "updating first name",
    #         "lastName": "updating last name",
    #         "email": "TDD4lyfe@unittest.com"
    #     }

    #     fake_uuid = uuid.uuid4()
    #     response = self.client.post("/api/author/{}".format(fake_uuid), 
    #         data=updated_profile, content_type="application/json")

    #     self.assertEqual(response.status_code, 400)
    #     self.assertEqual(json.loads(response.content), "Error: You do not have permission to update")

    # def test_post_wrong_author(self):
    #     self.client.login(username=self.username, password=self.password)

    #     updated_profile = {
    #         "displayName": "updating display name",
    #         "github": "http://www.github.com/updated_in_test",
    #         "bio": "updating bio",
    #         "firstName": "updating first name",
    #         "lastName": "updating last name",
    #         "email": "TDD4lyfe@unittest.com"
    #     }

    #     response = self.client.post("/api/author/{}".format(self.authorProfile2.id), 
    #         data=updated_profile, content_type="application/json")

    #     self.assertEqual(response.status_code, 400)
    #     self.assertEqual(json.loads(response.content), "Error: You do not have permission to edit this profile")
