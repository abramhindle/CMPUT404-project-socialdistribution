# Tests for the /service/author/{AUTHOR_ID}

from presentation.Serializers.author_sereializer import AuthorSerializer
from django.test import TestCase, Client
from presentation.models import Author
from django.contrib.auth.models import User
from presentation.Tests.test_helper import initial_author_field, initial_user_field, initial_post_author_field

# initialize the APIClient app
client = Client()


class AuthorTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(**initial_user_field())
        self.someone = Author.objects.create(**initial_author_field(self.user))

    def test_post_author(self):
        response = client.post(
            'http://127.0.0.1:8000/author/', data=initial_post_author_field())
        self.assertEqual(response.status_code, 200)

    # def test_get_author_by_id(self):
    #     author = Author.objects.get(id=self.someone.id)
    #     response = client.get(f'{self.someone.id}/')  # TODO: 404
    #     self.assertEqual(response.status_code, 200)
    #     serializer = AuthorSerializer(author)
    #     self.assertEqual(response.data, serializer.data)
