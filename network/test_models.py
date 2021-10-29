from django.test import TestCase
from .models import temp
from .models import Author
from .models import FriendRequest
from django.contrib.auth.models import User

# https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django/Testing
class AuthorModelTest(TestCase):
    def setUp(self):
        
        User.objects.create_user('testuser', 'test@example.com', 'testpassword', id = 103)
        Author.objects.create(uuid = '02c965fb-5b6d-4315-a012-2b5e1bfa28ad',
        id = "http://plurr.herokuapp.com/author/02c965fb-5b6d-4315-a012-2b5e1bfa28ad",
        url = "http://plurr.herokuapp.com/author/02c965fb-5b6d-4315-a012-2b5e1bfa28ad",
        host = "http://plurr.herokuapp.com",
        displayName= "Big Bob",
        github = None, 
        profileImage = None,
        user_id = 103)
        
    def test_displayName_label(self):
        author = Author.objects.get(uuid='02c965fb-5b6d-4315-a012-2b5e1bfa28ad')
        field_label = author._meta.get_field('displayName').verbose_name
        self.assertEqual(field_label, 'displayName')

    def test_id_label(self):
        author = Author.objects.get(uuid='02c965fb-5b6d-4315-a012-2b5e1bfa28ad')
        field_label = author._meta.get_field('id').verbose_name
        self.assertEqual(field_label, 'id')

    def test_url_label(self):
        author = Author.objects.get(uuid='02c965fb-5b6d-4315-a012-2b5e1bfa28ad')
        field_label = author._meta.get_field('url').verbose_name
        self.assertEqual(field_label, 'url')

    def test_host_label(self):
        author = Author.objects.get(uuid='02c965fb-5b6d-4315-a012-2b5e1bfa28ad')
        field_label = author._meta.get_field('url').verbose_name
        self.assertEqual(field_label, 'url')

    def test_type_label(self):
        author = Author.objects.get(uuid='02c965fb-5b6d-4315-a012-2b5e1bfa28ad')
        field_label = author._meta.get_field('type').verbose_name
        self.assertEqual(field_label, 'type')
    
    def test_github_label(self):
        author = Author.objects.get(uuid='02c965fb-5b6d-4315-a012-2b5e1bfa28ad')
        field_label = author._meta.get_field('github').verbose_name
        self.assertEqual(field_label, 'github')

    def test_uuid_label(self):
        author = Author.objects.get(uuid='02c965fb-5b6d-4315-a012-2b5e1bfa28ad')
        field_label = author._meta.get_field('uuid').verbose_name
        self.assertEqual(field_label, 'uuid')
    
    def test_profileImage_label(self):
        author = Author.objects.get(uuid='02c965fb-5b6d-4315-a012-2b5e1bfa28ad')
        field_label = author._meta.get_field('profileImage').verbose_name
        self.assertEqual(field_label, 'profileImage')
    
    def test_user_label(self):
        author = Author.objects.get(uuid='02c965fb-5b6d-4315-a012-2b5e1bfa28ad')
        field_label = author._meta.get_field('user').verbose_name
        self.assertEqual(field_label, 'user')
    
    def test_displayName_max_length(self):
        author = Author.objects.get(uuid='02c965fb-5b6d-4315-a012-2b5e1bfa28ad')
        max_length = author._meta.get_field('displayName').max_length
        self.assertEqual(max_length, 100)
    
    def test_type_max_length(self):
        author = Author.objects.get(uuid='02c965fb-5b6d-4315-a012-2b5e1bfa28ad')
        max_length = author._meta.get_field('displayName').max_length
        self.assertEqual(max_length, 100)
    
    def test_host_ends_with_slash(self):
        author = Author.objects.get(uuid='02c965fb-5b6d-4315-a012-2b5e1bfa28ad')
        host = author.host
        self.assertEqual(host[-1],'/')

# class FriendRequest(Model):
#     type = models.CharField(default='follow', max_length=100)
#     summary = models.CharField(null=True, max_length=500)
#     actor = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='actor')
#     object = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='object')

class FriendRequestModelTest(TestCase):
    def setUp(self):
        User.objects.create_user('testuser2', 'test2@example.com', 'testpassword2', id = 103)
        Author.objects.create(uuid = '02c965fb-5b6d-4315-a012-2b5e1bfa28ad',
        id = "http://plurr.herokuapp.com/author/02c965fb-5b6d-4315-a012-2b5e1bfa28ad",
        url = "http://plurr.herokuapp.com/author/02c965fb-5b6d-4315-a012-2b5e1bfa28ad",
        host = "http://plurr.herokuapp.com",
        displayName= "Big Bob",
        github = None, 
        profileImage = None,
        user_id = 103)

        User.objects.create_user('testuser1', 'test1@example.com', 'testpassword1', id = 104)
        Author.objects.create(uuid = '02c965fb-9d03-748c-012a-2b5e1bfa28ad',
        id = "http://plurr.herokuapp.com/author/02c965fb-9d03-748c-012a-2b5e1bfa28ad",
        url = "http://plurr.herokuapp.com/author/02c965fb-9d03-748c-012a-2b5e1bfa28ad",
        host = "http://plurr.herokuapp.com/",
        displayName= "tiny Bob",
        github = None, 
        profileImage = None,
        user_id = 104)

        FriendRequest.objects.create(type = 'follow', 
        summary = 'this is a summary', 
        actor = Author.objects.get(uuid='02c965fb-5b6d-4315-a012-2b5e1bfa28ad'), 
        object = Author.objects.get(uuid='02c965fb-9d03-748c-012a-2b5e1bfa28ad'))

    def test_type_label(self):
        request = FriendRequest.objects.get(actor = '02c965fb-5b6d-4315-a012-2b5e1bfa28ad', object = '02c965fb-9d03-748c-012a-2b5e1bfa28ad')
        field_label = request._meta.get_field('type').verbose_name
        self.assertEqual(field_label, 'type')
    
    def test_summary_label(self):
        request = FriendRequest.objects.get(actor = '02c965fb-5b6d-4315-a012-2b5e1bfa28ad', object = '02c965fb-9d03-748c-012a-2b5e1bfa28ad')
        field_label = request._meta.get_field('summary').verbose_name
        self.assertEqual(field_label, 'summary')

    def test_actor_label(self):
        request = FriendRequest.objects.get(actor = '02c965fb-5b6d-4315-a012-2b5e1bfa28ad', object = '02c965fb-9d03-748c-012a-2b5e1bfa28ad')
        field_label = request._meta.get_field('actor').verbose_name
        self.assertEqual(field_label, 'actor')
    
    def test_object_label(self):
        request = FriendRequest.objects.get(actor = '02c965fb-5b6d-4315-a012-2b5e1bfa28ad', object = '02c965fb-9d03-748c-012a-2b5e1bfa28ad')
        field_label = request._meta.get_field('object').verbose_name
        self.assertEqual(field_label, 'object')

# class TempTest(TestCase):
#     def setUp(self):
#         temp.objects.create(displayName = 'bigBob')
    
#     def test_display_name(self):
#         temp.objects.get(id=1)
#         field = temp._meta.get_field('displayName').verbose_name
#         self.assertEqual(field, 'displayName')