from django.test import TestCase
from  webserver.models import Author, FollowRequest
from rest_framework.test import APITestCase
from rest_framework import status
from unittest import mock


class AuthorTestCase(TestCase):
    def test_author_creation(self):
        Author.objects.create(display_name="Mark",username ="mmcgoey")
        Author.objects.create(display_name="Author2",username="auth2")
        author_mark = Author.objects.get(display_name ="Mark")
        self.assertEqual(author_mark.username,"mmcgoey")
        author_two = Author.objects.get(username="auth2")
        self.assertEqual(author_two.display_name,"Author2")


class FollowRequestTestCase(TestCase):
    def test_follow_request_deletion(self):
        """When sender is deleted, the associated follow request is also deleted"""
        author1 = Author.objects.create(display_name="Mark",username ="mmcgoey")
        author2 = Author.objects.create(display_name="Author2",username="auth2")
        FollowRequest.objects.create(sender=author1,receiver=author2)
        
        self.assertEqual(FollowRequest.objects.count(),1)
        author1.delete()
        self.assertEqual(FollowRequest.objects.count(), 0)


class AuthorsViewTestCase(APITestCase):
    def test_requests_require_authentication(self):
        """TODO"""
        pass

    def test_get(self):
        # create some authors
        Author.objects.create(username="author_1", display_name="author_1")
        Author.objects.create(username="author_2", display_name="author_2")
        Author.objects.create(username="author_3", display_name="author_3")
        
        url = "/authors/"
        self.client.force_authenticate(user=mock.Mock())
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)
        author_1 = response.data[0]
        self.assertEqual(author_1["display_name"], "author_1")

class AuthorDetailView(APITestCase):
    def test_requests_require_authentication(self):
        """TODO"""
        pass
        
    def test_get(self):
        author_1 = Author.objects.create(username="author_1", display_name="author_1")
        url = f'/authors/{author_1.id}/'
        self.client.force_authenticate(user=mock.Mock())
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

class AuthorRegistrationTestCase(APITestCase):
    def test_register_successful(self):
        request_payload = {
            "username": "author_1",
            "display_name": "best_author",
            "password": "password",
            "password2": "password"
        }
        response = self.client.post("/register/", data=request_payload, format="json")
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual("best_author", response.data["display_name"])
    
    def test_register_with_duplicate_username(self):
        Author.objects.create(username="author_1", display_name="author_1")
        request_payload = {
            "username": "author_1",
            "display_name": "best_author",
            "password": "password",
            "password2": "password"
        }
        response = self.client.post("/register/", data=request_payload, format="json")
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
    
    def test_register_with_mismatched_passwords(self):
        request_payload = {
            "username": "author_1",
            "display_name": "best_author",
            "password": "password",
            "password2": "other password"
        }
        response = self.client.post("/register/", data=request_payload, format="json")
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
    
    def test_register_with_incomplete_data(self):
        # password2 missing
        request_payload = {
            "username": "author_1",
            "display_name": "best_author",
            "password": "password"
        }
        response = self.client.post("/register/", data=request_payload, format="json")
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)


class LoginTestCase(APITestCase):
    def test_login_with_valid_credentials(self):
        author = Author.objects.create(username="author_1", display_name="author_1")
        author.set_password("pass123")
        author.save()

        request_payload = {"username": "author_1", "password": "pass123"}
        response = self.client.post("/login/", data=request_payload, format="json")
        self.assertEqual(status.HTTP_200_OK, response.status_code)
    
    def test_login_with_invalid_credentials(self):
        request_payload = {"username": "author_1", "password": "pass123"}
        response = self.client.post("/login/", data=request_payload, format="json")
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)
    
    def test_login_with_incomplete_request_payload(self):
        request_payload = {"username": "author_1"}
        response = self.client.post("/login/", data=request_payload, format="json")
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)


class LogoutTestCase(APITestCase):
    def test_logout(self):
        """Always logs out a request"""
        response = self.client.post("/logout/")
        self.assertEqual(status.HTTP_200_OK, response.status_code)
