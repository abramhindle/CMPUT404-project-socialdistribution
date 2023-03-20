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
            'author':author_data,
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

        # TODO:extract the post ID from the response
        
        post_id = str(Post.objects.all()[0].id)

        # test the get
        response = self.client.get(url+post_id+'/')
        
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertContains(response,"testing testy test")

    

       
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
            'author':author_data,
            'type':'post',
            'title':'test',
            'description':'testing testy test',
            'contentType':'image/png;base64',
            'content':'test',
            'image':base64_image
        }
        # test the POST to the posts URL, this time with an image in the object
        response = self.client.post(url,json.dumps(post_data),content_type="application/json")
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertContains(response,"testing testy test")

        # TODO:same post ID extraction step as the above
        post_id = '???'

        # test the GET and make sure that the image is in there. if it's there, it's rendered
        response = self.client.get(url+post_id+'/')
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertContains(response,"testing testy test")

        # TODO: test private posts
    

    def test_comments(self):
        return

    def test_likes(self):
        return
    

