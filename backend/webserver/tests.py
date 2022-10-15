from django.test import TestCase
from  webserver.models import Author, FollowRequest, Follow

# Writing useless tests to learn testing in django

class AuthorTestCase(TestCase):
    def setUp(self):
        Author.objects.create(display_name="Mark",github_handle ="mmcgoey")
        Author.objects.create(display_name="Author2",github_handle="auth2")

    
    def test_authors(self):
        author_mark = Author.objects.get(display_name ="Mark")
        self.assertEqual(author_mark.github_handle,"mmcgoey")
        author_two = Author.objects.get(github_handle="auth2")
        self.assertEqual(author_two.display_name,"Author2")
        
   


class FollowRequestTestCase(TestCase):
    def setUp(self):
        author1 = Author.objects.create(display_name="Mark",github_handle ="mmcgoey")
        author2 = Author.objects.create(display_name="Author2",github_handle="auth2")

        FollowRequest.objects.create(sender=author1,receiver=author2)
        

    
    def test_follow_request(self):
        """When sender is deleted the associated follow request is also deleted"""
        self.assertEqual(FollowRequest.objects.count(),1)
        sender = FollowRequest.objects.all()[0].sender
        sender.delete()
        self.assertEqual(FollowRequest.objects.count(), 0)


# Create your tests here.
