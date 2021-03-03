from rest_framework.test import APITestCase
from socialdistribution.models import Comment

class CommentTests(APITestCase):
    url = "/service/author/"
    post_data = {
        "title":"My Post",
        "source":"http://hello.com",
        "origin":"http://hello.com",
        "description":"My post",
        "contentType":"text/plain",
        "content":"blah",
        "visibility":"PUBLIC",
        "unlisted": False
    }

    account_data = {
        "email":"test@gmail.com", 
        "password":"pass", 
        "username":"Alice", 
        "github":""
    }

    comment_data = {
    "author_write_comment_ID":"",
    "comment": "I am a comment"
    }


    def create_account(self):
        # create author account
        response = self.client.post(self.url, self.account_data)
        self.assertEqual(response.status_code, 201)
        return response.data['authorID']

    def create_post(self):
        authorID = self.create_account()
        post_url = self.url + authorID + "/posts/"
        response = self.client.post(post_url, self.post_data)
        self.assertEqual(response.status_code, 201)
        return_data = {}
        return_data['post_url'] = post_url
        return_data['authorID'] = authorID
        return_data['postID'] = response.data['postID']
        return return_data
    
    def test_create_comment(self):
        # write a comment of the post
        get_data = self.create_post()
        post_url = get_data['post_url']
        authorID = get_data['authorID']
        postID = get_data['postID']
        comment_url = post_url+postID+'/comments/'
        self.comment_data["author_write_comment_ID"] = authorID
        response = self.client.post(comment_url, self.comment_data)
        self.assertEqual(response.status_code, 201)
        return_data = {}
        return_data['comment_url'] = comment_url
        return return_data

    
    def test_get_comments(self):
        # get comments of the post
        get_data = self.test_create_comment()
        comment_url = get_data['comment_url']
        response = self.client.get(comment_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['count'] ,1)