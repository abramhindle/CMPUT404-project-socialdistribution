from django.test import TestCase
from webserver.models import Author, FollowRequest, Inbox, Follow
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
        
        url = "/api/authors/"
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
        url = f'/api/authors/{author_1.id}/'
        self.client.force_authenticate(user=mock.Mock())
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["display_name"], "author_1")
    
    def test_get_404(self):
        """If an author requested does not exist, should return 404"""
        fake_id = 500124540593854
        url = f'/api/authors/{fake_id}/'
        self.client.force_authenticate(user=mock.Mock())
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        
    
    def test_post_all_fields(self):
        """POST request works on all editable data fields"""
        author_1 = Author.objects.create()
        url = f'/api/authors/{author_1.id}/'
        self.client.force_authenticate(user=mock.Mock())
        payload = {
            "display_name": "Mark McGoey",
            "profile_image": "No image",
            "github_handle": "mmcgoey"
        }
        response = self.client.post(url,data=payload)
        self.assertEqual(response.data["display_name"], "Mark McGoey")
        self.assertEqual(response.data["profile_image"], "No image")
        self.assertEqual(response.data["github_handle"], "mmcgoey")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    
    
    def test_post_no_fields(self):
        author_1 = Author.objects.create()
        url = f'/api/authors/{author_1.id}/'
        self.client.force_authenticate(user=mock.Mock())
        payload = {}
        response = self.client.post(url,data=payload)
        self.assertEqual(response.data["display_name"], "")
        self.assertEqual(response.data["profile_image"], "")
        self.assertEqual(response.data["github_handle"], "")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    
    def test_partial_post(self):
        """POST request can handle partial update"""
        author_1 = Author.objects.create()
        url = f'/api/authors/{author_1.id}/'
        payload = {
            "display_name": "Mark McGoey",
            "github_handle": "mmcgoey"
        }
        self.client.force_authenticate(user=mock.Mock())
        response = self.client.post(url,data=payload)
        self.assertEqual(response.data["display_name"], "Mark McGoey")
        self.assertEqual(response.data["profile_image"], "")
        self.assertEqual(response.data["github_handle"], "mmcgoey")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        
    
    def test_post_404(self):
        """If an author to be updated does not exist, should return 404"""
        fake_id = 500124540593854
        url = f'/api/authors/{fake_id}/'
        payload = {
            "display_name": "Mark McGoey",
            "profile_image": "No image",
            "github_handle": "mmcgoey"
        }
        self.client.force_authenticate(user=mock.Mock())
        response = self.client.post(url,data=payload)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_post_non_editable_fields(self):
        author_1 = Author.objects.create()
        url = f'/api/authors/{author_1.id}/'
        new_id = 500124540593854
        new_url = f'/api/authors/{new_id}/'
        payload = {
            "id":new_id,
            "url":new_url
        }
        self.client.force_authenticate(user=mock.Mock())
        response = self.client.post(url,data=payload)
        
        self.assertEqual(response.data["id"], author_1.id)
        self.assertEqual(response.data["url"],'http://testserver'+url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class AuthorRegistrationTestCase(APITestCase):
    def test_register_successful(self):
        request_payload = {
            "username": "author_1",
            "display_name": "best_author",
            "password": "password",
            "password2": "password"
        }
        response = self.client.post("/api/register/", data=request_payload, format="json")
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
        response = self.client.post("/api/register/", data=request_payload, format="json")
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
    
    def test_register_with_mismatched_passwords(self):
        request_payload = {
            "username": "author_1",
            "display_name": "best_author",
            "password": "password",
            "password2": "other password"
        }
        response = self.client.post("/api/register/", data=request_payload, format="json")
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
    
    def test_register_with_incomplete_data(self):
        # password2 missing
        request_payload = {
            "username": "author_1",
            "display_name": "best_author",
            "password": "password"
        }
        response = self.client.post("/api/register/", data=request_payload, format="json")
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)


class LoginTestCase(APITestCase):
    def test_login_with_valid_credentials(self):
        author = Author.objects.create(username="author_1", display_name="author_1")
        author.set_password("pass123")
        author.save()

        request_payload = {"username": "author_1", "password": "pass123"}
        response = self.client.post("/api/login/", data=request_payload, format="json")
        self.assertEqual(status.HTTP_200_OK, response.status_code)
    
    def test_login_with_invalid_credentials(self):
        request_payload = {"username": "author_1", "password": "pass123"}
        response = self.client.post("/api/login/", data=request_payload, format="json")
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)
    
    def test_login_with_incomplete_request_payload(self):
        request_payload = {"username": "author_1"}
        response = self.client.post("/api/login/", data=request_payload, format="json")
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)


class LogoutTestCase(APITestCase):
    def test_logout(self):
        """Always logs out a request"""
        response = self.client.post("/api/logout/")
        self.assertEqual(status.HTTP_200_OK, response.status_code)


class FollowRequestProcessorTestCase(APITestCase):
    def setUp(self):
        self.resource_name = "follow-requests"

    def test_create_follow_request_and_update_inbox(self):
        author_1 = Author.objects.create(username="author_1", display_name="author_1")
        author_2 = Author.objects.create(username="author_2", display_name="author_2")
        payload = {
            "type": "follow",
            "sender": {
                "url": f'http://127.0.0.1:5054/authors/{author_1.id}/',
                "id": author_1.id,
            },
            "receiver": {
                "url": f'http://127.0.0.1:5054/authors/{author_2.id}/',
                "id": author_2.id,
            }
        }
        self.assertEqual(0, FollowRequest.objects.count())
        url = f'/api/authors/{author_2.id}/inbox/'
        self.client.force_authenticate(user=mock.Mock())
        response = self.client.post(url, data=payload, format="json")

        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(1, FollowRequest.objects.count())
        fr = FollowRequest.objects.first()
        self.assertEqual(author_1, fr.sender)
        self.assertEqual(author_2, fr.receiver)

        self.assertEqual(1, Inbox.objects.count())
        inbox = Inbox.objects.first()
        self.assertEqual(author_2, inbox.target_author)
        self.assertEqual(author_1, inbox.follow_request_sender)
    
    def test_duplicate_follow_request_is_not_allowed(self):
        """It should raise an error when you try to create a follow request that already exists"""
        author_1 = Author.objects.create(username="author_1", display_name="author_1")
        author_2 = Author.objects.create(username="author_2", display_name="author_2")
        FollowRequest.objects.create(sender=author_1, receiver=author_2)
        self.assertEqual(1, FollowRequest.objects.count())

        payload = {
            "type": "follow",
            "sender": {
                "url": f'http://127.0.0.1:5054/authors/{author_1.id}',
                "id": author_1.id,
            },
            "receiver": {
                "url": f'http://127.0.0.1:5054/authors/{author_2.id}',
                "id": author_2.id,
            }
        }
        url = f'/api/authors/{author_2.id}/inbox/'
        self.client.force_authenticate(user=mock.Mock())
        response = self.client.post(url, data=payload, format="json")
        self.assertEqual(status.HTTP_409_CONFLICT, response.status_code)
        self.assertEqual(1, FollowRequest.objects.count())
        
    def test_reverse_follow_request_is_allowed(self):
        """Author 1 can send a follow request to Author 2 and Author 2 can send a follow request to Author 1"""
        author_1 = Author.objects.create(username="author_1", display_name="author_1")
        author_2 = Author.objects.create(username="author_2", display_name="author_2")
        FollowRequest.objects.create(sender=author_1, receiver=author_2)
        self.assertEqual(1, FollowRequest.objects.count())
        
        payload = {
            "type": "follow",
            "sender": {
                "url": f'http://127.0.0.1:5054/authors/{author_2.id}',
                "id": author_2.id,
            },
            "receiver": {
                "url": f'http://127.0.0.1:5054/authors/{author_1.id}',
                "id": author_1.id,
            }
        }
        url = f'/api/authors/{author_1.id}/inbox/'
        self.client.force_authenticate(user=mock.Mock())
        response = self.client.post(url, data=payload, format="json")
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(2, FollowRequest.objects.count())
        fr = FollowRequest.objects.last()
        self.assertEqual(author_2, fr.sender)
        self.assertEqual(author_1, fr.receiver)

    def test_cannot_send_follow_request_to_self(self):
        """Author cannot send follow request to themselves"""
        author_1 = Author.objects.create(username="author_1", display_name="author_1")
        author_2 = Author.objects.create(username="author_2", display_name="author_2")
        self.assertEqual(0, FollowRequest.objects.count())
        payload = {
            "sender": {
                "url": f'http://127.0.0.1:5054/authors/{author_1.id}',
                "id": author_1.id,
            },
            "receiver": {
                "url": f'http://127.0.0.1:5054/authors/{author_1.id}',
                "id": author_1.id,
            }
        }
        url = f'/api/authors/{author_1.id}/inbox/'
        self.client.force_authenticate(user=mock.Mock())
        response = self.client.post(url, data=payload, format="json")
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertEqual(0, FollowRequest.objects.count())
    
    def test_request_not_valid_when_required_fields_are_not_given(self):
        """Proper serializer fields need to be given"""
        author_1 = Author.objects.create(username="author_1", display_name="author_1")
        author_2 = Author.objects.create(username="author_2", display_name="author_2")
        # 'url' field is missing in the sender
        payload = {
            "type": "follow",
            "sender": {
                "id": author_1.id,
            },
            "receiver": {
                "url": f'http://127.0.0.1:5054/authors/{author_1.id}',
                "id": author_1.id,
            }
        }
        url = f'/api/authors/{author_1.id}/inbox/'
        self.client.force_authenticate(user=mock.Mock())
        response = self.client.post(url, data=payload, format="json")
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertEqual(0, FollowRequest.objects.count())

    def test_request_is_valid_when_extra_fields_are_given(self):
        author_1 = Author.objects.create(username="author_1", display_name="author_1")
        author_2 = Author.objects.create(username="author_2", display_name="author_2")
        self.assertEqual(0, FollowRequest.objects.count())
        payload = {
            "type": "follow",
            "sender": {
                "url": f'http://127.0.0.1:5054/authors/{author_1.id}',
                "id": author_1.id,
                "display_name": "author_1",
                "profile_image": "",
                "github_handle": ""
            },
            "receiver": {
                "url": f'http://127.0.0.1:5054/authors/{author_2.id}',
                "id": author_2.id,
                "display_name": "author_2",
                "profile_image": "",
                "github_handle": ""
            }
        }
        
        url = f'/api/authors/{author_2.id}/inbox/'
        self.client.force_authenticate(user=mock.Mock())
        response = self.client.post(url, data=payload, format="json")

        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(1, FollowRequest.objects.count())
        fr = FollowRequest.objects.first()
        self.assertEqual(author_1, fr.sender)
        self.assertEqual(author_2, fr.receiver)
    
    def test_cannot_send_follow_request_if_already_a_follower(self):
        """Cannot send a follow request to someone who's already being followed"""
        author_1 = Author.objects.create(username="author_1", display_name="author_1")
        author_2 = Author.objects.create(username="author_2", display_name="author_2")
        Follow.objects.create(follower=author_1, followee=author_2)
        self.assertEqual(1, Follow.objects.count())
        
        payload = {
            "type": "follow",
            "sender": {
                "url": f'http://127.0.0.1:5054/authors/{author_1.id}',
                "id": author_1.id,
            },
            "receiver": {
                "url": f'http://127.0.0.1:5054/authors/{author_2.id}',
                "id": author_2.id,
            }
        }
        url = f'/api/authors/{author_2.id}/inbox/'
        self.client.force_authenticate(user=mock.Mock())
        response = self.client.post(url, data=payload, format="json")
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertEqual(0, FollowRequest.objects.count())


class FollowRequestsTestCase(APITestCase):
    def setUp(self):
        self.resource_name = "follow-requests"
    
    def test_author_has_multiple_follow_requests(self):
        author_1 = Author.objects.create(username="author_1", display_name="author_1")
        author_2 = Author.objects.create(username="author_2", display_name="author_2")
        author_3 = Author.objects.create(username="author_3", display_name="author_3")
        FollowRequest.objects.create(sender=author_2, receiver=author_1)
        FollowRequest.objects.create(sender=author_3, receiver=author_1)
        
        url = f'/api/authors/{author_1.id}/follow-requests/'
        self.client.force_authenticate(user=mock.Mock())
        response = self.client.get(url)

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(2, len(response.data))
        fr1 = response.data[0]
        fr2 = response.data[1]
        expected_fields = ['id', 'url', 'display_name', 'profile_image', 'github_handle']
        for field in expected_fields:
            self.assertTrue(field in fr1)
            self.assertTrue(field in fr2)

        self.assertTrue(fr1['url'].startswith('http'))
        self.assertTrue(fr1['url'].endswith('/authors/2/'))
        self.assertEqual(author_2.id, fr1['id'])
        self.assertEqual(author_3.id, fr2['id'])

    def test_author_has_no_follow_requests(self):
        author_1 = Author.objects.create(username="author_1", display_name="author_1")
        url = f'/api/authors/{author_1.id}/follow-requests/'
        self.client.force_authenticate(user=mock.Mock())
        response = self.client.get(url)

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(0, len(response.data))

    def test_author_does_not_exist(self):
        author_1 = Author.objects.create(username="author_1", display_name="author_1")
        url = f'/api/authors/{author_1.id + 1}/follow-requests/'
        self.client.force_authenticate(user=mock.Mock())
        response = self.client.get(url)
        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)


class FollowersViewTestCase(APITestCase):
    def test_author_has_multiple_followers(self):
        author_1 = Author.objects.create(username="author_1", display_name="author_1")
        author_2 = Author.objects.create(username="author_2", display_name="author_2")
        author_3 = Author.objects.create(username="author_3", display_name="author_3")
        Follow.objects.create(followee=author_1, follower=author_2)
        Follow.objects.create(followee=author_1, follower=author_3)
        
        url = f'/api/authors/{author_1.id}/followers/'
        self.client.force_authenticate(user=mock.Mock())
        response = self.client.get(url)
        
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(2, len(response.data))
        f1 = response.data[0]
        f2 = response.data[1]
        expected_fields = ['id', 'url', 'display_name', 'profile_image', 'github_handle']
        for field in expected_fields:
            self.assertTrue(field in f1)
            self.assertTrue(field in f2)

        self.assertTrue(f1['url'].startswith('http'))
        self.assertTrue(f1['url'].endswith('/authors/2/'))
        self.assertEqual(author_2.id, f1['id'])
        self.assertEqual(author_3.id, f2['id'])
    
    def test_author_has_no_followers(self):
        author_1 = Author.objects.create(username="author_1", display_name="author_1")
        url = f'/api/authors/{author_1.id}/followers/'
        self.client.force_authenticate(user=mock.Mock())
        response = self.client.get(url)

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(0, len(response.data))


class FollowersDetailViewTestCase(APITestCase):
    def test_author_accepts_a_follow_request(self):
        author_1 = Author.objects.create(username="author_1", display_name="author_1")
        author_2 = Author.objects.create(username="author_2", display_name="author_2")
        FollowRequest.objects.create(sender=author_2, receiver=author_1)
        self.assertEqual(1, FollowRequest.objects.count())
        
        # author_1 accepts the request
        url = f'/api/authors/{author_1.id}/followers/{author_2.id}/'
        payload = {
            "follow_request_sender": {
                "url": f'http://127.0.0.1:5054/authors/{author_2.id}',
                "id": author_2.id,
            }
        }
        self.client.force_authenticate(user=mock.Mock())
        response = self.client.put(url, data=payload, format="json")
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(1, Follow.objects.count())
        self.assertEqual(0, FollowRequest.objects.count())

        new_follow = Follow.objects.first()
        self.assertEqual(author_1, new_follow.followee)
        self.assertEqual(author_2, new_follow.follower)
        
    def test_follow_request_does_not_exist(self):
        """Author cannot accept a follow request when a request does not exist to begin with"""
        author_1 = Author.objects.create(username="author_1", display_name="author_1")
        author_2 = Author.objects.create(username="author_2", display_name="author_2")
        self.assertEqual(0, FollowRequest.objects.count())

        url = f'/api/authors/{author_1.id}/followers/{author_2.id}/'
        payload = {
            "follow_request_sender": {
                "url": f'http://127.0.0.1:5054/authors/{author_2.id}',
                "id": author_2.id,
            }
        }
        self.client.force_authenticate(user=mock.Mock())
        response = self.client.put(url, data=payload, format="json")
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertEqual(0, Follow.objects.count())
    
    def test_valid_request_data_is_not_given(self):
        author_1 = Author.objects.create(username="author_1", display_name="author_1")
        author_2 = Author.objects.create(username="author_2", display_name="author_2")
        FollowRequest.objects.create(sender=author_2, receiver=author_1)
        self.assertEqual(1, FollowRequest.objects.count())
        
        # author_1 accepts the request
        url = f'/api/authors/{author_1.id}/followers/{author_2.id}/'
        payload = {
            "follow_request_sender": {
                "id": author_2.id,
            }
        }
        self.client.force_authenticate(user=mock.Mock())
        response = self.client.put(url, data=payload, format="json")
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertEqual(0, Follow.objects.count())
    
    def test_author_does_not_exist(self):
        author_1 = Author.objects.create(username="author_1", display_name="author_1")
        url = f'/api/authors/{author_1.id}/followers/{author_1.id + 1}/'
        payload = {
            "follow_request_sender": {
                "url": f'http://127.0.0.1:5054/authors/{author_1.id + 1}',
                "id": author_1.id + 1,
            }
        }
        self.client.force_authenticate(user=mock.Mock())
        response = self.client.put(url, data=payload, format="json")
        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)
    
    def test_reverse_follow_is_allowed(self):
        author_1 = Author.objects.create(username="author_1", display_name="author_1")
        author_2 = Author.objects.create(username="author_2", display_name="author_2")
        Follow.objects.create(follower=author_2, followee=author_1)
        FollowRequest.objects.create(sender=author_1, receiver=author_2)
        self.assertEqual(1, Follow.objects.count())
        self.assertEqual(1, FollowRequest.objects.count())
        
        # author_2 accepts the request
        url = f'/api/authors/{author_2.id}/followers/{author_1.id}/'
        payload = {
            "follow_request_sender": {
                "url": f'http://127.0.0.1:5054/authors/{author_1.id}',
                "id": author_1.id,
            }
        }
        self.client.force_authenticate(user=mock.Mock())
        response = self.client.put(url, data=payload, format="json")
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(2, Follow.objects.count())
        self.assertEqual(0, FollowRequest.objects.count())

    def test_get(self):
        """The given foreign_author_id is a follower of author_id"""
        author_1 = Author.objects.create(username="author_1", display_name="author_1")
        author_2 = Author.objects.create(username="author_2", display_name="author_2")
        Follow.objects.create(follower=author_2, followee=author_1)
        url = f'/api/authors/{author_1.id}/followers/{author_2.id}/'
        self.client.force_authenticate(user=mock.Mock())
        response = self.client.get(url)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
    
    def test_get_404(self):
        """the given foreign_author_id is NOT a follower of author_id"""
        author_1 = Author.objects.create(username="author_1", display_name="author_1")
        author_2 = Author.objects.create(username="author_2", display_name="author_2")
        url = f'/api/authors/{author_1.id}/followers/{author_2.id}/'
        self.client.force_authenticate(user=mock.Mock())
        response = self.client.get(url)
        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)
    
    def test_delete(self):
        """Remove foreign_author_id as a follower of author_id"""
        author_1 = Author.objects.create(username="author_1", display_name="author_1")
        author_2 = Author.objects.create(username="author_2", display_name="author_2")
        Follow.objects.create(follower=author_2, followee=author_1)
        self.assertEqual(1, Follow.objects.count())

        url = f'/api/authors/{author_1.id}/followers/{author_2.id}/'
        self.client.force_authenticate(user=mock.Mock())
        response = self.client.delete(url)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(0, Follow.objects.count())
    
    def test_delete_404(self):
        """Cannot remove a follower that does not exist"""
        author_1 = Author.objects.create(username="author_1", display_name="author_1")
        author_2 = Author.objects.create(username="author_2", display_name="author_2")
        url = f'/api/authors/{author_1.id}/followers/{author_2.id}/'
        self.client.force_authenticate(user=mock.Mock())
        response = self.client.get(url)
        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)
