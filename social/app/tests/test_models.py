from django.contrib.auth.models import User
from django.test import TestCase

from social.app.models.author import Author
from social.app.models.node import Node


class NodeTestCase(TestCase):
    def setUp(self):
        Node.objects.create(name="Test", host="http://www.socdis.com/", service_url="http://api.socdis.com/")

    def test_to_str_method(self):
        node = Node.objects.get(name="Test")
        self.assertEqual(str(node), "Test (http://www.socdis.com/; http://api.socdis.com/)")


class AuthorTestCase(TestCase):
    def setUp(self):
        self.node = Node.objects.create(name="Test", host="http://www.socdis.com/",
                                        service_url="http://api.socdis.com/", local=True)

        user = User.objects.create_user("test1", "test@test.com", "pass1")
        self.author = Author.objects.get(user__id=user.id)
        self.author.displayName = "Bobbert"
        self.author.user.last_name = "McBob"
        self.author.user.first_name = "Bob"

    def test_author_str(self):
        self.assertEquals(str(self.author), "McBob, Bob (Bobbert)")

    def test_author_url(self):
        self.assertEquals(str(self.author.get_id_url()), self.node.service_url + "authors/" + str(self.author.id) + "/")

    def test_author_does_not_follow(self):
        user = User.objects.create_user("test2", "test@test.com", "pass1")
        author = Author.objects.get(user__id=user.id)

        self.assertFalse(self.author.follows(author))

    def test_author_does_follow(self):
        user = User.objects.create_user("test2", "test@test.com", "pass1")
        author = Author.objects.get(user__id=user.id)
        self.author.followed_authors.add(author)

        self.assertTrue(self.author.follows(author))
