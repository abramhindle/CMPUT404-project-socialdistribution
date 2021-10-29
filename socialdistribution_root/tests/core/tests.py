from django.http.request import HttpRequest
from django.test import RequestFactory, TestCase
from django.urls import reverse
from apis.authors.views import author
from apps.core.serializers import AuthorSerializer
from apps.core.models import Author
from rest_framework.parsers import JSONParser

class CoreViewTests(TestCase):

    def test_index_renders(self):
        response = self.client.get(reverse('core:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "This is the home page.")
