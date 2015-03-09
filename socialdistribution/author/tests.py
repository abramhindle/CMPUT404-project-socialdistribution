from django.test import TestCase
from django.test import Client


class AuthorTestCase(TestCase):
    def setup(self):
        user = User.objects.create_user(username="myuser",
                                        password="mypassword")

        author = Author.objects.create(user=user, github_user='mygithubuser')

    def test_login_redirect(self):
        """Testing login for redirection for invalid user"""
        c = Client()
        response = c.post('/', {'username': 'myuser',
                                'password': 'wrongpassword'})

        self.assertNotEqual(response.status_code, 302)
