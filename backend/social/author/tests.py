from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from .models import Author

# check create author + get author(s)
class TestCreateAuthor(APITestCase):
    # tests the get and multi-get function of the author view
    def test_get(self):
        # create the author first so we can have the ID
        create_author = Author.objects.create(displayName='sugon')
        Author.objects.create(displayName='sawcon')
        test_id = str(create_author).split('(')
        test_id = test_id[-1].strip(')')
        user_url = reverse('authors:get_authors') + test_id + '/'
        # the single get
        response = self.client.get(user_url)
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertContains(response,"sugon")
        # the multi-get
        response = self.client.get(reverse('authors:get_authors'))
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertContains(response,"sugon")
        self.assertContains(response,"sawcon")

    # tests the put function of the author view
    def test_put(self):
        # create the author first so we can have the ID
        create_author = Author.objects.create(displayName='sugon')
        test_id = str(create_author).split('(')
        test_id = test_id[-1].strip(')')
        user_url = reverse('authors:get_authors') + test_id + '/'
        # test the put
        response = self.client.put(user_url,{'displayName':'sawcon'})
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertContains(response,"sawcon")
