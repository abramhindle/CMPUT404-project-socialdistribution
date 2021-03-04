from rest_framework.test import APITestCase
from socialdistribution.models import Post

class PostTests(APITestCase):
    url = "/service/author/"
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
    def create_account(self):
        # create author account
        response = self.client.post(self.url, {"email":"test@gmail.com", "password":"pass", "username":"Alice", "github":""})
        self.assertEqual(response.status_code, 201)
        return response.data['authorID']

    def test_create_post(self):
        authorID = self.create_account()
        post_url = self.url + authorID + "/posts/"
        response = self.client.post(post_url, self.data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Post.objects.count(), 1)
    
    def test_get_all_posts(self):
        authorID = self.create_account()
        post_url = self.url + authorID + "/posts/"
        data2 = {
            "title":"My Second Post",
            "source":"http://hello.com",
            "origin":"http://hello.com",
            "description":"My post",
            "contentType":"text/plain",
            "content":"blah",
            "visibility":"PUBLIC",
            "unlisted": False
        }
        # create two posts
        self.client.post(post_url, self.data)
        self.client.post(post_url, data2)
        
        # posts are sort by published time, most recent first
        response = self.client.get(post_url)
        self.assertEqual(len(response.data["posts"]), 2)
        self.assertEqual(response.data["posts"][0]["title"], "My Second Post")
        self.assertEqual(response.data["posts"][1]["title"], "My Post")

    def create_post(self):
        authorID = self.create_account()
        post_url = self.url + authorID + "/posts/"
        response = self.client.post(post_url, self.data) # create post
        postID = response.data["postID"]
        return authorID, postID

    def test_get_post_detail(self):
        authorID, postID = self.create_post()
        post_detail_url = self.url + authorID + "/posts/" + postID + "/"

        # get post
        response = self.client.get(post_detail_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["title"], "My Post")

        # change postID and check 404
        postID = postID.upper()
        invalid_url = self.url + authorID + "/posts/" + postID + "/"
        response = self.client.get(invalid_url)
        self.assertEqual(response.status_code, 404)

    def test_put_post(self):
        authorID = self.create_account()
        postID = "a8416c4a-56fb-4dfc-b0a1-486ab55608a8"
        post_detail_url = self.url + authorID + "/posts/" + postID + "/"
        response = self.client.put(post_detail_url, self.data) # put post
        self.assertEqual(response.data["title"], "My Post")

        response = self.client.put(post_detail_url, self.data) # postID occupied
        self.assertEqual(response.status_code, 400)

    def test_update_post(self):
        authorID, postID = self.create_post()
        post_detail_url = self.url + authorID + "/posts/" + postID + "/"

        modified_data = {
            "title":"Modified Post",
            "source":"http://hello.com",
            "origin":"http://hello.com",
            "description":"My post",
            "contentType":"text/plain",
            "content":"blah",
            "visibility":"PUBLIC",
            "unlisted": False
        }

        response = self.client.post(post_detail_url, modified_data)
        self.assertEqual(response.data["title"], "Modified Post")

        # change postID and check 404
        postID = postID.upper()
        invalid_url = self.url + authorID + "/posts/" + postID + "/"
        response = self.client.post(invalid_url)
        self.assertEqual(response.status_code, 404)

    def test_delete_post(self):
        authorID, postID = self.create_post()
        post_detail_url = self.url + authorID + "/posts/" + postID + "/"
        response = self.client.get(self.url + authorID + "/posts/") # create post
        self.assertEqual(len(response.data["posts"]), 1) # number of posts = 1

        # delete post
        self.client.delete(post_detail_url)
        response = self.client.get(self.url + authorID + "/posts/")
        self.assertEqual(len(response.data["posts"]), 0) # number of posts = 0

        # delete post that doesn't exist
        response = self.client.delete(post_detail_url)
        self.assertEqual(response.status_code, 404)
