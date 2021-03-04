from rest_framework.test import APITestCase
from socialdistribution.models import Follow

class FollowerTests(APITestCase):
    url = "/service/author/"
    def create_account(self):
        # create author account
        response = self.client.post(self.url, {"email":"test@gmail.com", "password":"pswd", "username":"Alice", "github":""})
        self.assertEqual(response.status_code, 201)
        return response.data['authorID']

    def test_followers(self):
        # create two followers
        authorID = self.create_account()
        add_follower_url = self.url + authorID + "/followers/"
        data1 = {"email":"test1@gmail.com", "password":"pass", "username":"Crystal", "github":""}
        data2 = {"email":"test2@gmail.com", "password":"pass", "username":"Bob", "github":""}
        response1 = self.client.post(self.url, data1)
        response2 = self.client.post(self.url, data2)
        follower1 = response1.data['authorID']
        follower2 = response2.data['authorID']
        url1 = add_follower_url + follower1 + "/"
        url2 = add_follower_url + follower2 + "/"

        # add two followers
        self.client.put(url1)
        self.client.put(url2)

        # check the list of followers
        response = self.client.get(add_follower_url)
        items = response.data["items"]
        self.assertEqual(items[0]["displayName"], "Crystal")
        self.assertEqual(items[1]["displayName"], "Bob")

        # check if these two are followers
        response1 = self.client.get(url1)
        response2 = self.client.get(url2)
        self.assertEqual(response1.data["message"], "True")
        self.assertEqual(response2.data["message"], "True")

        # delete 1st follower and check

        # check if deleted successfully
        response = self.client.delete(url1)
        self.assertEqual(response.data["message"], "Success")

        # check if still a follower
        response1 = self.client.get(url1)
        self.assertEqual(response1.data["message"], "False")

        # check the list of follower
        response = self.client.get(add_follower_url)
        items = response.data["items"]
        self.assertEqual(len(items), 1)
