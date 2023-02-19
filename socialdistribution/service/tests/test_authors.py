from django.test import *
from service.models.author import Author
from service.views.author import *

class AuthorTests(TestCase):

    def setUp(self):
        self.author = Author.objects.create(displayName = "Joe Guy", host = "http://localhost:8000")
        self.request_factory = RequestFactory()
    
    def test_get_single_author(self):
        get_request = self.request_factory.get("/service/")
        author_response = single_author(get_request, self.author._id)

        self.assertEqual(author_response.status_code, 200)

        author = json.loads(author_response.content)

        self.assertEqual(author["id"], str(self.author._id))
        self.assertEqual(author["displayName"], self.author.displayName)
        self.assertEqual(author["url"], f"{self.author.host}/authors/{self.author._id}")

    def test_post_single_author(self):
        
        body = {
            "displayName": "Some Other Guy"
        }

        post_request = self.request_factory.post("/service/", data=json.dumps(body), content_type = CONTENT_TYPE_JSON)

        post_response = single_author(post_request, self.author._id)

        self.assertEqual(post_response.status_code, 202)

        author = Author.objects.get(_id=self.author._id)
        print(author.displayName)

        return
