from django.test import TestCase
from .models import Author 

class ModelTesting(TestCase):

    def setUp(self):
        self.author = Author.objects.create(
                type = "author",
                home_host = "http://127.0.0.1:5454/",
                display_name = "Gandalf the Grey",
                profile_url = "http://127.0.0.1:5454/authors/9de17f29c12e8f97bcbbd34cc908f1baba40658e",
                author_github = "http://github.com/gandalfthegrey",
                profile_image = "https://i.imgur.com/k7XVwpB.jpeg"
                )

    def test_author_model_is_valid(self):
        d = self.author
        self.assertTrue(isinstance(d, Author))

    def test_author_model_str(self):
        d = self.author
        self.assertEqual(str(d), "Gandalf the Grey")
