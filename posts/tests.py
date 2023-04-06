from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from .models import Post
from .models import Author,Post
from PIL import Image
from urllib import parse
import json
import base64
test_image = Image.open(r"media/test_img/test_img.png")
# Create your tests here.

# test post (normal and image) functionalities, comments, and likes
class TestPosts(APITestCase):
    # tests the http post and get functionality for posts
    def test_posts_post_and_get(self):
        # create the author of the posts + extract the URL
        create_author = Author.objects.create(displayName='sugon')
        test_name = str(create_author).split('(')
        test_id = test_name[-1].strip(')')
        # get url for the user to make posts at
        url = reverse('posts:posts',kwargs={'pk_a':test_id})
        # set up the json object with that data
        author_data = {
            'id':test_id,
            'displayName':test_name[0].strip(),
        }
        post_data = {
            'type':'post',
            'title':'test',
            'description':'testing testy test',
            'contentType':'text/plain',
            'content':'test'
        }
        
        # test the post
        response = self.client.post(url,json.dumps(post_data),content_type="application/json")
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertContains(response,"testing testy test")

        # extract the post ID from the response
        post_id = str(Post.objects.all()[0].id)
        
        # test the get
        url = url+post_id+'/'
        response = self.client.get(url)
        
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertContains(response,"testing testy test")

        #Testing editing a shared post
        post_data = {
            'title':'testUpdated',
            'description':'testing testy testUpdated',
        }

        response = self.client.post(url,json.dumps(post_data),content_type="application/json")
        self.assertEqual(response.status_code,status.HTTP_405_METHOD_NOT_ALLOWED)

        #Testing DELETE for an individual post
        response = self.client.delete(url)
        self.assertEqual(response.status_code,status.HTTP_204_NO_CONTENT)

        #Testing PUT where the postiD is custom
        url = reverse('posts:detail',kwargs={'pk_a':test_id,'pk':'MyCustomID'})
        post_data = {
            'title':'custom title',
            'description':'testing testy test',
            'contentType':'text/plain',
            'content':'test'
        }
        response = self.client.put(url,json.dumps(post_data),content_type="application/json")
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertContains(response,"custom title")

       
    # as image posts share the same POST process up to the serializer,
    # but a different GET from views to render the image
    # might need to add auth cases later on...
    def test_image_posts(self):
        # create the author of the posts + extract the URL
        create_author = Author.objects.create(displayName='sugon')
        test_name = str(create_author).split('(')
        test_id = test_name[-1].strip(')')
        # get url for the user to make posts at
        url = reverse('posts:posts',kwargs={'pk_a':test_id})
        # test image converted to base64
        with open("media/test_img/test_img.png", "rb") as png_image:
            base64_image = base64.b64encode(png_image.read())
        # set up the json object with that data
        author_data = {
            'id':test_id,
            'displayName':test_name[0].strip(),
        }
        post_data = {
            'type':'post',
            'title':'test',
            'description':'testing testy test',
            'contentType':'image/png',
            'content':'test',
            'image':str(base64_image)
        }
        # test the POST to the posts URL, this time with an image in the object
        response = self.client.post(url,json.dumps(post_data),content_type="application/json")
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertContains(response,"testing testy test")

        # same post ID extraction step as the above
        post_id = str(Post.objects.all()[0].id)

        # test the GET and make sure that the image is in there. if it's there, it's rendered
        response = self.client.get(url+post_id+'/')
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertContains(response,"testing testy test")

        # TODO: test private posts
    
    def test_comments(self):
        '''Testing get and post of comments
            have also included tests for individual comment get'''

        create_author = Author.objects.create(displayName='sugon')
        test_name = str(create_author).split('(')
        test_id = test_name[-1].strip(')')
        create_author2 = Author.objects.create(displayName='sawcon')
        test_name2= str(create_author2).split('(')
        test_id2 = test_name2[-1].strip(')')
        # get url for the user to make posts at
        url = reverse('posts:posts',kwargs={'pk_a':test_id})
        # set up the json object with that data
        
        post_data = {
            'type':'post',
            'title':'test',
            'description':'testing testy test',
            'contentType':'text/plain',
            'content':'test'
        }
        
        # test the post
        response = self.client.post(url,json.dumps(post_data),content_type="application/json")
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertContains(response,"testing testy test")
        post_id = str(Post.objects.all()[0].id)
        url = reverse('posts:comments',kwargs={'pk_a':test_id,'pk':post_id})
        comment_data = {
            "author_id":test_id2,
            "comment":"test2"
        }
        response = self.client.post(url,json.dumps(comment_data),content_type="application/json")
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertContains(response,"test2")

        #test the get
        response = self.client.get(url)
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertContains(response,"test2")

        #test individual comment get
        commenturl = response.json()['results'][0]['id']
        response = self.client.get(commenturl)
        self.assertEqual(response.status_code,status.HTTP_200_OK)

        #liking the comment
        url = reverse("authors:inbox",kwargs={"pk_a":test_id})
        like_data = {"type": "Like", "author_id": test_id2, "object" :commenturl}
        response = self.client.post(url,json.dumps(like_data),content_type="application/json") 
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        response = self.client.get(url)
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertContains(response,"sawcon Likes your post")

    def test_likes(self):
        '''incomplete'''
        create_author = Author.objects.create(displayName='sugon')
        test_name = str(create_author).split('(')
        test_id = test_name[-1].strip(')')
        create_author2 = Author.objects.create(displayName='sawcon')
        test_name2= str(create_author2).split('(')
        test_id2 = test_name2[-1].strip(')')
        # get url for the user to make posts at
        url = reverse('posts:posts',kwargs={'pk_a':test_id})
        # set up the json object with that data
        
        post_data = {
            'type':'post',
            'title':'test',
            'description':'testing testy test',
            'contentType':'text/plain',
            'content':'test'
        }
        
        # test the post
        response = self.client.post(url,json.dumps(post_data),content_type="application/json")
        
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertContains(response,"testing testy test")
        post_id = str(Post.objects.all()[0].id)

        #POST request for the like
        url = reverse("authors:inbox",kwargs={"pk_a":test_id})
        posturl = response.json()['id']
        like_data = {"type": "Like", "author_id": test_id2, "object" :posturl}
        response = self.client.post(url,json.dumps(like_data),content_type="application/json")
        self.assertEqual(response.status_code,status.HTTP_200_OK)


        #NEEDS FIXING ( )
        url = posturl + "/likes/"
        response = self.client.get(url)
        self.assertEqual(response.status_code,status.HTTP_200_OK)
   



        #testing liked posts of an author
        url = reverse("authors:get_liked",kwargs={"pk_a":test_id2})
        response = self.client.get(url)
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertContains(response,"sawcon Likes your post")
        
        
        return
    
