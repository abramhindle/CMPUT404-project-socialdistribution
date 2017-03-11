from django.test import TestCase
from dashboard.models import Node


class NodeTestCase(TestCase):
    def setUp(self):
        Node.objects.create(name="Test", host="http://www.socdis.com/", service_url="http://api.socdis.com/")

    def test_to_str_method(self):
        node = Node.objects.get(name="Test")
        self.assertEqual(str(node), "Test (http://www.socdis.com/; http://api.socdis.com/)")