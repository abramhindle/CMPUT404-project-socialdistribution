from rest_framework.test import APITestCase
from socialdistribution.models import Inbox

class InboxTests(APITestCase):
    url = "/service/author/"
    def create_account(self):
        # create author account
        response = self.client.post(self.url, {"email":"test@gmail.com", "password":"pass", "username":"Alice", "github":""})
        self.assertEqual(response.status_code, 201)
        return response.data['authorID']

    def create_post(self):
        data = {
            "title":"My Post",
            "source":"http://hello.com",
            "origin":"http://hello.com",
            "description":"My post",
            "contentType":"text/plain",
            "content":"blah",
            "visibility":"PUBLIC",
            "unlisted": False
        }
        authorID = self.create_account()
        post_url = self.url + authorID + "/posts/"
        response = self.client.post(post_url, data) # create post
        postID = response.data["postID"]
        return authorID, postID

    def test_post_to_inbox(self):
        authorID, postID = self.create_post()
        inbox_url = self.url + authorID + "/inbox/"
        # send post to inbox
        self.client.post(inbox_url, {"type":"post", "postID":postID})

        # send like to inbox
        response = self.client.post(self.url, {"email":"test2@gmail.com", "password":"pass", "username":"Laura", "github":""})
        author_like_ID = response.data['authorID']
        like = {
            "type":"like",
            "at_context": "https://www.w3.org/ns/activitystreams",
            "summary": "Laura likes your post",
            "author_like_ID": author_like_ID,
            "postID": postID
        }
        self.client.post(inbox_url, like)
        self.assertEqual(Inbox.objects.count(), 1)
        inbox = Inbox.objects.get(authorID=authorID)
        self.assertEqual(len(inbox.items), 2)

    def test_get_inbox(self):
        authorID, postID = self.create_post()
        inbox_url = self.url + authorID + "/inbox/"
        # send post to inbox
        self.client.post(inbox_url, {"type":"post", "postID":postID})

        # send like to inbox
        response = self.client.post(self.url, {"email":"test2@gmail.com", "password":"pass", "username":"Laura", "github":""})
        author_like_ID = response.data['authorID']
        like = {
            "type":"like",
            "at_context": "https://www.w3.org/ns/activitystreams",
            "summary": "Laura likes your post",
            "author_like_ID": author_like_ID,
            "postID": postID
        }
        self.client.post(inbox_url, like)
        
        response = self.client.get(inbox_url) # get from inbox
        items = response.data["items"]
        self.assertEqual(items[0]["type"], "like")
        self.assertEqual(items[0]["summary"], "Laura likes your post")
        self.assertEqual(items[1]["type"], "post")
        self.assertEqual(items[1]["description"], "My post")
        