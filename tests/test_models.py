import uuid
from django.test import TestCase
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from backend.models import Author

class AuthorModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        uuid_list = [
            "95a1e643-180c-4de6-8fc5-9cb48a216fbe",
            "856c692d-2514-4d06-80fc-4c4312188db3",
        ]
        number_of_authors = len(uuid_list)
        User.objects.bulk_create([
            User(username="AuthorViewTest_{}".format(idx),
            password=make_password("Margret Thatcher"),
            is_active=True
            ) for idx in range(number_of_authors)
        ])
        for author_id in range(number_of_authors):
            Author.objects.create(
                id=uuid_list[author_id],
                user=User.objects.get(username="AuthorViewTest_{}".format(author_id)),
                display_name="Test unit{}".format(author_id),
                url="http://127.0.0.1:8000/author/{}".format(uuid_list[author_id]),
                host="http://127.0.0.1:8000/",
            )
    def test_display_name(self):
        author = Author.objects.get(id="95a1e643-180c-4de6-8fc5-9cb48a216fbe")
        field_label = author.display_name
        self.assertEqual(field_label, 'Test unit0')
        author = Author.objects.get(id="856c692d-2514-4d06-80fc-4c4312188db3")
        field_label = author.display_name
        self.assertEqual(field_label, 'Test unit1')

    