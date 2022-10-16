from django.test import TestCase
from  webserver.models import Author, FollowRequest
from rest_framework.test import APITestCase
from rest_framework import status


class AuthorTestCase(TestCase):
    def test_author_creation(self):
        Author.objects.create(display_name="Mark",github_handle ="mmcgoey")
        Author.objects.create(display_name="Author2",github_handle="auth2")
        author_mark = Author.objects.get(display_name ="Mark")
        self.assertEqual(author_mark.github_handle,"mmcgoey")
        author_two = Author.objects.get(github_handle="auth2")
        self.assertEqual(author_two.display_name,"Author2")


class FollowRequestTestCase(TestCase):
    def test_follow_request_deletion(self):
        """When sender is deleted, the associated follow request is also deleted"""
        author1 = Author.objects.create(display_name="Mark",github_handle ="mmcgoey")
        author2 = Author.objects.create(display_name="Author2",github_handle="auth2")
        FollowRequest.objects.create(sender=author1,receiver=author2)
        
        self.assertEqual(FollowRequest.objects.count(),1)
        author1.delete()
        self.assertEqual(FollowRequest.objects.count(), 0)


class AuthorsViewTestCase(APITestCase):
    def test_get(self):
        # create some authors
        Author.objects.create(display_name="author_1")
        Author.objects.create(display_name="author_2")
        Author.objects.create(display_name="author_3")
        
        url = "/authors/"
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)
        author_1 = response.data[0]
        self.assertEqual(author_1["display_name"], "author_1")

class AuthorDetailView(APITestCase):
    def test_get(self):
        author_1 = Author.objects.create(display_name="author_1")
        url = f'/authors/{author_1.id}/'
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["display_name"], "author_1")
    
    def test_get_404(self):
        """If an author requested does not exist, should return 404"""
        pass    # TODO
    
    def test_post(self):
        """POST request works on all editable data fields"""
        pass    # TODO
    
    def test_partial_post(self):
        """POST request can handle partial update"""
        pass    # TODO
    
    def test_post_404(self):
        """If an author to be updated does not exist, should return 404"""
        pass    # TODO