from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from .models import Post
from .models import Author
from PIL import Image
from urllib import parse
import json
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
        # set up the test json object with that data
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
        
        response = self.client.post(url,json.dumps(post_data),content_type="application/json")
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertContains(response,"testing testy test")

        response = self.client.get(url)
    
    # as image posts share the same POST process up to the serializer,
    # but a different GET from views to render the image
    def test_image_posts(self):
        
        return

    def test_comments(self):
        return
    
    def test_likes(self):
        return
    

