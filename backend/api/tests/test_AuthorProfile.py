from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import RequestsClient
from ..serializers import AuthorProfileSerializer
from ..models import AuthorProfile
import json
import uuid


class AuthorProfileCase(TestCase):
    client = RequestsClient()
    username = "test123"
    password = "pw123"

    def setUp(self):
        self.user = User.objects.create_user(username=self.username, password=self.password)
        self.authorProfile = AuthorProfile.objects.create(
                                            user = self.user,
                                            host="http://localhost.com",
                                            displayName="unit test displayname",
                                            github="http://www.github.com/htruong1",
                                            bio="this is a unit test",
                                            firstName="my first name",
                                            lastName="my gucci last name",
                                            email="iloveTDD@TDD.com"
        )

    # def test_get_author_with_invalid_id(self):
    #     self.client.login(username=self.username, password=self.password)
    #     fake_uuid = uuid.uuid4()
    #     response = self.client.get("/api/author/{}".format(fake_uuid))
    #     self.assertEqual(response.status_code, 400)

    # def test_get_valid_id_with_no_auth(self):
    #     response = self.client.get("/api/author/{}".format(self.authorProfile.id))
    #     self.assertEqual(response.status_code, 403)

    # def test_get_author_profile_with_auth(self):
    #     self.client.login(username=self.username, password=self.password)
    #     response = self.client.get("/api/author/{}".format(self.authorProfile.id))
    #     self.assertEqual(response.status_code, 200)

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