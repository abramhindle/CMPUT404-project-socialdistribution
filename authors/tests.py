import json
import base64
from copy import deepcopy
from django.test import TestCase
from rest_framework.test import APIClient, APIRequestFactory, force_authenticate
from rest_framework_simplejwt.tokens import RefreshToken

from django.contrib.auth.models import User
from authors.models import Author
from authors.serializers import AuthorSerializer, FriendRequestSerializer
from authors.views import InboxListView

# Create your tests here.

client = APIClient()  # the mock http client
factory = APIRequestFactory()


def client_with_auth(user, client):
    refresh = RefreshToken.for_user(user)
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
    return client


class FriendRequestTestCase(TestCase):
    DATA = {
        "type": "Follow",
        "summary": "Greg wants to follow Lara",
        "actor": {
            "type": "author",
            "id": "http://127.0.0.1:5454/author/1d698d25ff008f7538453c120f581471",
            "url": "http://127.0.0.1:5454/author/1d698d25ff008f7538453c120f581471",
            "host": "http://127.0.0.1:5454/",
            "displayName": "Greg Johnson",
            "github": "http://github.com/gjohnson"
            # TODO
            # "profileImage": "https://i.imgur.com/k7XVwpB.jpeg"
        },
        "object": {
            "type": "author",
            "id": "http://127.0.0.1:5454/author/9de17f29c12e8f97bcbbd34cc908f1baba40658e",
            "host": "http://127.0.0.1:5454/",
            "displayName": "Lara Croft",
            "url": "http://127.0.0.1:5454/author/9de17f29c12e8f97bcbbd34cc908f1baba40658e",
            "github": "http://github.com/laracroft"
            # TODO: Image from a public domain
            # "profileImage": "https://i.imgur.com/k7XVwpB.jpeg"
        }
    }

    def setUp(self):
        # create an object author first, mock an existing local author
        local_author = deepcopy(self.DATA['object'])
        local_author['id'] = '9de17f29c12e8f97bcbbd34cc908f1baba40658e'
        object = AuthorSerializer(data=local_author)
        if object.is_valid():
            author = object.save()
            user = User.objects.create(
                username='test_user', password='test_pass')
            author.user = user
            author.save()

    def test_deserializing_friend_request(self):
        # try parse the data
        serialzier = FriendRequestSerializer(data=deepcopy(self.DATA))
        if not serialzier.is_valid():
            print(serialzier.errors)
        assert serialzier.is_valid()
        f = serialzier.save()
        assert f.actor.display_name == self.DATA['actor']['displayName']
        assert f.object.display_name == self.DATA['object']['displayName']

    def test_inbox_post(self):
        user = User.objects.get(username='test_user')
        new_client = client_with_auth(user, client)
        _ = new_client.post(
            '/author/9de17f29c12e8f97bcbbd34cc908f1baba40658e/inbox/', data=self.DATA, format='json')
        _ = new_client.post(
            '/author/9de17f29c12e8f97bcbbd34cc908f1baba40658e/inbox/', data=self.DATA, format='json')

        inbox_items = new_client.get(
            '/author/9de17f29c12e8f97bcbbd34cc908f1baba40658e/inbox/', format='json')
        assert len(inbox_items.data) == 2
        self.assertDictEqual(inbox_items.data[0], self.DATA)

        local_author = Author.objects.get(
            id='9de17f29c12e8f97bcbbd34cc908f1baba40658e')
        self.assertEqual(len(local_author.inbox_objects.all()), 2)


class AuthorSerializerTestCase(TestCase):
    # mock the raw requests.data['actor'] dict, not validated yet.
    FOREIGN_AUTHOR_A_DATA = {
        'type': 'author',
        'id': 'http://localhost:8001/author/123321123321',
        'url': 'http://localhost:8001/author/123321123321',
        'host': 'http://localhost:8001/',
        'displayName': 'Foreign Author A',
        'github': 'https://github.com/asasdf@#$!d'
    }

    FOREIGN_AUTHOR_B_DATA = {
        'type': 'author',
        'id': 'http://localhost:8001/author/123321123321',
        'url': 'http://localhost:8001/author/123321123321',
        'host': 'http://localhost:8001/',
        'displayName': 'Foreign Author B'
    }

    def test_create_external_author_object_happy(self):
        foreign_author_data = self.FOREIGN_AUTHOR_A_DATA

        s = AuthorSerializer(data=foreign_author_data)

        assert s.is_valid()
        foreign_author = s.save()  # an Author object

        assert foreign_author.id == self.FOREIGN_AUTHOR_A_DATA['id']
        assert foreign_author.url == self.FOREIGN_AUTHOR_A_DATA['url']
        assert foreign_author.display_name == self.FOREIGN_AUTHOR_A_DATA['displayName']
        assert foreign_author.host == self.FOREIGN_AUTHOR_A_DATA['host']
        assert foreign_author.github_url == self.FOREIGN_AUTHOR_A_DATA['github']
        assert foreign_author.user is None

    def test_create_external_author_object_bare(self):
        foreign_author_data = self.FOREIGN_AUTHOR_B_DATA

        s = AuthorSerializer(data=foreign_author_data)
        if not s.is_valid():
            print(s.errors)
        assert s.is_valid()
        foreign_author = s.save()  # an Author object

        assert foreign_author.id == self.FOREIGN_AUTHOR_B_DATA['id']
        assert foreign_author.url == self.FOREIGN_AUTHOR_B_DATA['url']
        assert foreign_author.host == self.FOREIGN_AUTHOR_B_DATA['host']
        assert foreign_author.display_name == self.FOREIGN_AUTHOR_B_DATA['displayName']
        assert foreign_author.user is None


class AuthorTestCase(TestCase):
    def setup_single_user_and_author(self):
        self.user = User.objects.create_user(
            'test_username', 'test_email', 'test_pass')
        self.author = Author.objects.create(
            user=self.user, display_name=self.user.username)

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

    def test_update_author_detail(self):
        # first register a user
        register_payload = {
            'username': 'test_register_simple_happy',
            'password': ';askdjfxzc0-v8923k5jm0-Z*xklcasxcKLjKj()*^$!^',
        }
        res = client.post('/register/', register_payload, format='json')
        '''
        expected sample response
        {
            "displayName": "LUcasdf",
            "github": "https://github.com/asdf",
            "host": "http://127.0.0.1:8000/register/",
            "id": "http://127.0.0.1:8000/author/8d2718f8-a957-418c-b826-f51bbb34f57f/",
            "type": "author",
            "url": "http://127.0.0.1:8000/author/8d2718f8-a957-418c-b826-f51bbb34f57f/"
        }
        '''
        assert res.data['author']['displayName'] == register_payload['username']
        assert res.data['author']['id'] == res.data['author']['url'] and res.data['author']['id'].startswith(
            'http')
        assert res.data['author']['type'] == 'author'
        assert res.data['author']['github'] is None
        assert res.status_code == 200

        # assert user is created correctly
        user = User.objects.get(username=register_payload['username'])
        assert user is not None

        # authenticate with jwt token
        authed_client = client_with_auth(user, client)
        # update details
        payload = {
            'displayName': 'Test Name',
            'github': 'https://github.com/asdfas'
        }
        res = authed_client.post(
            res.data['author']['id'], payload, format='json')
        assert res.data['displayName'] == payload['displayName']
        assert res.data['github'] == payload['github']
