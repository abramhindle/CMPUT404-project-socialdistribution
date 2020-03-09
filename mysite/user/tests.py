from django.test import TestCase, RequestFactory
from .models import User

# Create your tests here.
class UserTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_users_existence(self):
        user1 = User.objects.get(username="user1")
        self.assertEqual(user1.email, "user1@email.com")
