from django.test import TestCase
from django.urls import reverse

class CoreViewTests(TestCase):

    def test_index_renders(self):
        response = self.client.get(reverse('core:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "This is the home page.")