from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from .models import Post
from PIL import Image
test_image = Image.open(r"media/test_img/test_img.png")
# Create your tests here.

# test post creation

# test image post + proper base64 serialization
class ImagePostTestCase(APITestCase):

    def test_post_image(self):
        response = self.client.post(reverse('posts'),{
            'author':'jimbobpaulkevin',
            'categories':'',
            'title':'',
            'description':'',
            'contentType':'image/png;base64',
            'content':'',
            'image':test_image,
        })

        print(response)

    '''
    def test_image_is_serialized(self):
        base64_image = Post.objects.get(author='jimbobpaulkevin')
    '''