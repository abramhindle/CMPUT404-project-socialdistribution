from django.test import TestCase
from django.urls import reverse

class PostsViewTests(TestCase):

    # Not fine-tuned and will fail if you are logged in
    def test_index_renders(self):
        pass
        response = self.client.get(reverse('posts:index'))
        self.assertEqual(response.status_code, 200)
        # self.assertContains(response, "This will eventually be a list of public posts.")