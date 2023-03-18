from django.test import *
from service.models.author import Author
from django.contrib.auth.models import User
from service.views.author import *
from service.views.follower import *


class FollowTests(TestCase):

    def setUp(self):

        self.single_view = FollowerAPI()
        self.multiple_view = FollowersAPI()

        self.user1 = User.objects.create_user("joeguy", "joeguy@email.com", "12345")
        self.user2 = User.objects.create_user("somebody", "somebody@email.com", "1234")
        self.user3 = User.objects.create_user("hua", "hua@email.com", "123456")
        self.user4 = User.objects.create_user("check", "check@email.com", "1234567")


        self.author1 = Author.objects.create(displayName = "Joe Guy", host = "http://localhost:8000", user = self.user1)
        self.author2 = Author.objects.create(displayName = "Somebody Else", host = "http://localhost:8000", user = self.user2)
        self.author3 = Author.objects.create(displayName = "Hua", host = "http://localhost:8000", user = self.user3)
        self.author4 = Author.objects.create(displayName = "check", host = "http://localhost:8000", user = self.user4)

        self.author1.followers.add(self.author2)
        self.author1.followers.add(self.author3)
        self.author1.save()
    
        self.request_factory = RequestFactory()
    
    def tearDown(self):
        self.user1.delete()
        self.user2.delete()
        self.user3.delete()
        self.user4.delete()
        self.author1.delete()
        self.author2.delete()
        self.author3.delete()
        self.author4.delete()

    def test_get_single_follower(self):
        request = HttpRequest()
        request.method = "get"

        follow_response = self.single_view.get(request, self.author1._id, self.author3._id)
        
        self.assertEqual(follow_response.status_code, 200)

        author = json.loads(follow_response.content)

        self.assertEqual(author["id"], str(self.author3._id))
        self.assertEqual(author["displayName"], self.author3.displayName)
        self.assertEqual(author["host"], self.author3.host)

    def test_put_follower(self):
        request = HttpRequest()
        request.method = "put"

        put_response = self.single_view.put(request, self.author1._id, self.author4._id)
        self.assertEqual(put_response.status_code, 200)

        request = HttpRequest()
        request.method = "get"

        get_response = self.single_view.get(request, self.author1._id, self.author4._id)
        author = json.loads(get_response.content)

        self.assertEqual(author["id"], str(self.author4._id))

    def test_followers(self):
        request = HttpRequest()
        request.method = "get"

        followers_response = self.multiple_view.get(request, self.author1._id)

        self.assertEqual(followers_response.status_code, 200)

        json_paged = json.loads(followers_response.content)

        self.assertTrue("type" in json_paged) #payload should be structured with the correct fields
        self.assertTrue("items" in json_paged)

        payload_type = json_paged["type"]

        self.assertEqual(payload_type, "followers") #payload type should be marked as follower

        json_followers = json_paged["items"]

        self.assertTrue(len(json_followers), 2)

        self.assertEqual(json_followers[0]["id"], str(self.author3._id))
        self.assertEqual(json_followers[0]["displayName"], str(self.author3.displayName))
        self.assertEqual(json_followers[1]["id"], str(self.author2._id))
        self.assertEqual(json_followers[1]["displayName"], str(self.author2.displayName))

    