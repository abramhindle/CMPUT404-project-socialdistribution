from django.test import TestCase
from django.test import Client


class AuthorTestCase(TestCase):
    def setup(self):
        user = User.objects.create_user(username="myuser",
                                        password="mypassword")

        author = Author.objects.create(user=user, github_user='mygithubuser')

    def test_login_redirect(self):
        """Testing login for redirection of invalid user"""
        c = Client()
        response = c.post('/', {'username': 'myuser',
                                'password': 'wrongpassword'})

        self.assertNotEqual(response.status_code, 302)

    def test_logout_redirect(self):
        """Testing logout for redirection to index"""
        c = Client()
        response = c.get('/author/logout')

        self.assertEqual(response.status_code, 301)
