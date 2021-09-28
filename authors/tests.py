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
        pass

    def test_get_author_list(self):
        self.setup_single_user_and_author()
        res = client.get('/authors/', format='json')
        content = json.loads(res.content)

        # content should look like [{'id': 'adfsadfasdfasdf', 'displayName': 'test_username', 'url': '', 'host': '', 'user': 1, 'friends': []}]
        assert len(content) == 1

        # API fields as per spec, not model fields.
        assert content[0]['displayName'] == 'test_username'
        assert content[0]['id'] == str(self.author.id)
        assert res.status_code == 200
        
    def test_get_author_detail(self):
        self.setup_single_user_and_author()
        res = client.get(f'/author/{self.author.id}/', format='json')
        content = json.loads(res.content)

        # content should look like {'id': 'adfsadfasdfasdf', 'displayName': 'test_username', 'url': '', 'host': '', 'user': 1, 'friends': []}
        assert content['displayName'] == 'test_username'
        assert content['id'] == str(self.author.id)
        assert res.status_code == 200
        
