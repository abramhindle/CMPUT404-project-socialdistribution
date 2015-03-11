from django.test import TestCase
from django.core.files import File
from images.models import Image
 
class Test_image(TestCase):
    def test_upload(self):
        i1 = Image()
        i1.title = "aaa"
        i1.thumb = File(open("static/images/comments4.png"))
        i1.save()
        
        p = Image.objects.get(id=1).thumb.path
        
        self.failUnless(open(p), 'file not found')
# Create your tests here.
