from rest_framework.test import APITestCase
from socialdistribution.models import Inbox

class FRTests(APITestCase):
    url = "/service/author/"
    def create_accounts(self):
        # create author account
        response = self.client.post(self.url, {"email":"test@gmail.com", "password":"pswd", "username":"Alice", "github":""})
        self.assertEqual(response.status_code, 201)
        author = response.data['authorID']
        data = {"email":"test1@gmail.com", "password":"pass", "username":"Crystal", "github":""}
        response = self.client.post(self.url, data)
        follower = response.data['authorID']
        return author, follower

    def test_send_friend_request(self):
        authorID, follower = self.create_accounts()

        # send friend request
        add_fr_url = self.url + authorID + "/inbox/"
        response = self.client.post(add_fr_url, {"type":"follow", "new_follower_ID": follower})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["message"], "sent successfully!")

    def check_friend_request(self):
        authorID, follower = self.create_accounts()
        # check if the request is in inbox
        inbox_url = self.url + authorID + "/inbox/"
        response = self.client.post(inbox_url, data)
        items = response.data["items"]
        self.assertEqual(items["type"], "Follow")
        self.assertEqual(items["summary"], "Crystal wants to follow Alice")

    def check_accept_friend_request(self):
        authorID, follower = self.create_accounts()
        fr_url = self.url + authorID + "/inbox/friendrequest/" + follower + "/"
        response = self.client.post(add_fr_url, {"type":"accept"})
        self.assertEqual(response.data["message"], "Success!")
