from django.test import *
from service.models.author import Author
from django.contrib.auth.models import User
from service.views.author import *
import unittest
from unittest import mock

#mock helper
def mocked_requests_get(*args, **kwargs):
    class MockResponse:
        def __init__(self, json_data, status_code):
            self.json_data = json_data
            self.status_code = status_code

        def json(self):
            return self.json_data

    # if args[0] == 'http://someurl.com/test.json':
    #     return MockResponse({"key1": "value1"}, 200)
    # elif args[0] == 'http://someotherurl.com/anothertest.json':
    #     return MockResponse({"key2": "value2"}, 200)

    return MockResponse({}, 200)

class AuthorTests(unittest.TestCase):

    def setUp(self):

        self.single_view = SingleAuthor()
        self.multiple_view = MultipleAuthors()

        self.user1 = User.objects.create_user("joeguy", "joeguy@email.com", "12345")
        self.user2 = User.objects.create_user("somebody", "somebody@email.com", "1234")

        self.author1 = Author.objects.create(displayName = "Joe Guy", host = "http://localhost:8000", user = self.user1)
        self.author2 = Author.objects.create(displayName = "Somebody Else", host = "http://localhost:8000", user = self.user2)
        self.request_factory = RequestFactory()

    def tearDown(self):
        self.user1.delete()
        self.user2.delete()
        self.author1.delete()
        self.author2.delete()

    #@mock.patch('requests.get', side_effect=mocked_requests_get)
    def test_get_single_author(self):
        get_request = self.request_factory.get("/service/", user = self.user1)
        get_request.user = self.user1

        author_response = self.single_view.get(get_request, author_id=self.author1._id)

        self.assertEqual(author_response.status_code, 200)

        author = json.loads(author_response.content)

        self.assertEqual(author["id"], str(self.author1._id))
        self.assertEqual(author["displayName"], self.author1.displayName)
        self.assertEqual(author["url"], str(self.author1._id))

    #@mock.patch('requests.get', side_effect=mocked_requests_get)
    def test_post_single_author(self):

        body = {
            "displayName": "Some Other Guy"
        }

        post_request = self.request_factory.post("/service/", data=json.dumps(body), content_type = CONTENT_TYPE_JSON)
        post_request.user = self.user1

        post_response = self.single_view.post(post_request, author_id=self.author1._id)

        self.assertEqual(post_response.status_code, 202)

        author = Author.objects.get(_id=self.author1._id) #get the author object to check if the POST updated successfully

        self.assertEqual(author.displayName, body["displayName"]) # author.displayName should be the new value of displayName

    @mock.patch('requests.get', side_effect=mocked_requests_get)
    def test_get_multiple_authors(self, *args, **kwargs):
        get_multiple_request = self.request_factory.get("/service/", QUERY_STRING="page=1&size=2")
        get_multiple_request.user = self.user1
        authors_response = self.multiple_view.get(get_multiple_request)

        self.assertEqual(authors_response.status_code, 200)

        json_paged = json.loads(authors_response.content)

        self.assertTrue("type" in json_paged) #payload should be structured with the correct fields
        self.assertTrue("items" in json_paged)

        payload_type = json_paged["type"]

        self.assertEqual(payload_type, "author") #payload type should be marked as author

        json_authors = json_paged["items"]

        self.assertTrue(len(json_authors), 2)

        list(Author.objects.all())

        self.assertEqual(json_authors[0]["id"], str(self.author1._id))
        self.assertEqual(json_authors[0]["displayName"], str(self.author1.displayName))
        self.assertEqual(json_authors[1]["id"], str(self.author2._id))
        self.assertEqual(json_authors[1]["displayName"], str(self.author2.displayName))

    #use these once we get authentication working
    def test_get_author_unauthenticated(self):
        pass

    def test_post_author_unauthenticated(self):
        pass