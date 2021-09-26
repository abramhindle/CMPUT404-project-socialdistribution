import json
from django.test import TestCase
from rest_framework.test import APIClient

from django.contrib.auth.models import User
from authors.models import Author

# Create your tests here.

client = APIClient() # the mock http client

class AuthorTestCase(TestCase):
    def setup_single_user_and_author(self):
        self.user = User.objects.create_user('test_username', 'test_email', 'test_pass')
        self.author = Author.objects.create(user=self.user, display_name=self.user.username)
    def setUp(self):
        self.setup_single_user_and_author()

    def test_get_author_list(self):
        res = client.get('/authors/', format='json')
        content = json.loads(res.content)

        # content should look like [{'id': 'adfsadfasdfasdf', 'display_name': 'test_username', 'url': '', 'host': '', 'user': 1, 'friends': []}]
        assert len(content) == 1
        assert content[0]['display_name'] == 'test_username'
        assert content[0]['user'] == self.user.pk
        assert res.status_code == 200
        
    def test_get_author_detail(self):
        res = client.get(f'/author/{self.author.id}/', format='json')
        content = json.loads(res.content)

        # content should look like {'id': 'adfsadfasdfasdf', 'display_name': 'test_username', 'url': '', 'host': '', 'user': 1, 'friends': []}
        assert content['display_name'] == 'test_username'
        assert content['user'] == self.user.pk
        assert res.status_code == 200
        
