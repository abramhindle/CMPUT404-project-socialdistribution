from rest_framework.test import APITestCase
from socialdistribution.models import LikePost,LikeComment,Liked

class LikeTest(APITestCase):
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

    like_post_data = {
    "at_context":"http://hello.com",
    "summary": "post",
    "type":"like",
    "author_like_ID":"",
    "postID":""
    }

    like_comment_data = {
    "at_context":"http://hello.com",
    "summary": "comment",
    "type":"like",
    "author_like_ID":"",
    "commentID":"",
    "postID":""
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
    
    def create_comment(self):
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
        return_data['postID'] = postID
        return_data['authorID'] = authorID
        return_data['commentID'] = response.data['comment']['commentID']
        return return_data

    def test_like_post(self):
        #test like on a post
        get_data = self.create_post()
        authorID = get_data['authorID']
        postID = get_data['postID']
        self.like_post_data['author_like_ID'] = authorID
        self.like_post_data['postID'] = postID
        like_post_url = self.url+authorID+'/inbox/'
        response = self.client.post(like_post_url, self.like_post_data)
        self.assertEqual(response.status_code, 200)
        #test get like on the post
        like_post_url_get = self.url+authorID+'/posts/'+postID+'/likes/'
        response = self.client.get(like_post_url_get)
        self.assertEqual(response.status_code, 200)
    
    def test_like_comments(self):
        get_data = self.create_comment()
        authorID = get_data['authorID']
        postID = get_data['postID']
        commentID = get_data['commentID']
        self.like_comment_data['author_like_ID'] = authorID
        self.like_comment_data['postID'] = postID
        self.like_comment_data['commentID'] = commentID
        like_comment_url = self.url+authorID+'/inbox/'
        response = self.client.post(like_comment_url, self.like_comment_data)
        self.assertEqual(response.status_code, 200)
        #test get like on the comment
        like_comment_url_get = get_data['comment_url'] + commentID+ '/likes/'
        response = self.client.get(like_comment_url_get)
        self.assertEqual(response.status_code, 200)
            

