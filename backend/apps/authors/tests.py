from django.test import TestCase, Client

c = Client()

# Create your tests here.

# Test authors
class Author_TestCase(TestCase):
    def setUp(self) -> None:
        return super().setUp()
    
    def test_get_nonexisting_author(self):
        """GET /authors/-1/ (trying to get a non-existant author should return a 404 code)"""
        response = c.get('/authors/-1/')
        self.assertEqual(response.status_code, 404)

    def test_get_all_authors(self):
        """GET /authors/ (get all authors should return a 200 code)"""
        response = c.get('/authors/')
        self.assertEqual(response.status_code, 200)

    def test_post_invalid_author(self):
        """POST /authors/ (trying to create an invalid author should return a 400 code)"""
        # this is invalid because the github link must be <= 100 chars
        response = c.post('/authors/', {"github": "01234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789"})
        self.assertEqual(response.status_code, 400)

    # def test_create_author(self):
    #     """POST /authors/ (creating a valid author should return a 201 code)"""
    #     response = c.post('/authors/', {"displayName": "bob"})
    #     self.assertEqual(response.status_code, 201)

