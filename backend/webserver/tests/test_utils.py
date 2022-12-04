from django.test import TestCase
from webserver.utils import join_urls, get_post_id_from_url

class JoinUrlsTestCase(TestCase):
    def test_join_urls_works(self):
        result = join_urls("https://social-distribution-1.herokuapp.com/api", "authors/123/", "posts/")
        self.assertEqual("https://social-distribution-1.herokuapp.com/api/authors/123/posts", result)

    def test_join_urls_with_ending_slash(self):
        result = join_urls("https://social-distribution-1.herokuapp.com/api", "authors/123/", "posts/", 
                           ends_with_slash=True)
        self.assertEqual("https://social-distribution-1.herokuapp.com/api/authors/123/posts/", result)
    
    def test_get_post_id_from_url(self):
        result = get_post_id_from_url("https://social-distribution-1.herokuapp.com/api/authors/241/posts/123/")
        self.assertEqual("123", result)

    def test_get_post_id_from_url_with_no_url(self):
        result = get_post_id_from_url("123")
        self.assertEqual("123", result)
