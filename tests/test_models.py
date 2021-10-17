import uuid
from django.test import TestCase
from django.contrib.auth.models import User
from backend.models import Author

class AuthorModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        user = User.objects.create_user("TestUser")
        Author.objects.create(
            id="2f91a911-850f-4655-ac29-9115822c72a8",
            user=user,
            url="http://127.0.0.1:8000/author/2f91a911-850f-4655-ac29-9115822c72a8",
            host="http://127.0.0.1:8000/",
            display_name="Test unit",
        )
    def test_display_name(self):
        author = Author.objects.get(id="2f91a911-850f-4655-ac29-9115822c72a8")
        field_label = author.display_name
        self.assertEqual(field_label, 'Test unit')

    