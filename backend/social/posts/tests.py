from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from .models import Post
from PIL import Image
test_image = Image.open(r"media/test_img/test_img.png")
# Create your tests here.

# test post creation
class PostTestCase(APITestCase):
    def test_post(self):
        url = f'/posts/authors/3ec2d0f6-846b-4057-a1d5-aec1f4734740/posts/'
        response = self.client.post(url,{
            'author':'3ec2d0f6-846b-4057-a1d5-aec1f4734740',
            'categories':'test',
            'title':'test',
            'description':'test',
            'contentType':'image/png;base64',
            'content':'test',
            'image':test_image,
        })

# test image post + proper base64 serialization
class ImagePostTestCase(APITestCase):

    def test_post_image(self):
        url = f'/posts/authors/3ec2d0f6-846b-4057-a1d5-aec1f4734740/posts/'
        response = self.client.post(url,{
            'author':'3ec2d0f6-846b-4057-a1d5-aec1f4734740',
            'categories':'test',
            'title':'test',
            'description':'test',
            'contentType':'image/png;base64',
            'content':'test',
            'image':test_image,
        })

        #self.assertEqual(response.status_code,status.HTTP_200_OK)

    # def test_get_image(self):
    #    return