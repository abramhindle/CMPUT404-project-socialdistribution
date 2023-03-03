from django.test import TestCase, Client

c = Client()

# Create your tests here.

# Test posts
class Post_TestCase(TestCase):
    def setUp(self) -> None:
        return super().setUp()
    
    def test_get_posts_invalid_author(self):
        """GET /authors/-1/posts/ (get posts from invalid author should return 404 code)"""
        response = c.get(f'/authors/-1/posts/')
        self.assertEqual(response.status_code, 404)

    def test_get_invalid_post_invalid_author(self):
        """GET /authors/-1/posts/-1 (get invalid post from invalid author should return 404 code)"""
        response = c.get('/authors/-1/posts/-1')
        self.assertEqual(response.status_code, 404)

    # removed some tests that relied on author creation