from django.test import TestCase
from .models import Post
from .models import Author
from .models import FriendRequest
from django.contrib.auth.models import User
from datetime import datetime


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



class PostModelTest(TestCase):
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

        Post.objects.create( type = 'post',#, max_length=100)
            title = 'the universe is too big',
            uuid = 'f02b44c7-c5db-4a20-9651-7a0658085ee8',
            id = "http://plurr.herokuapp.com/author/02c965fb-5b6d-4315-a012-2b5e1bfa28ad/posts/f02b44c7-c5db-4a20-9651-7a0658085ee8",
            source = None,
            origin =None,
            description = "it's literally bigger than your mom",
            contentType = "text/plain",
            content = "and your mom is BIG, really big",
            author = Author.objects.get(uuid= '02c965fb-5b6d-4315-a012-2b5e1bfa28ad'),
            categories = '{web,tutorial}',
            count = 0,
            comments = None,
            published = datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            visibility = "PUBLIC",
            unlisted = True)

    def test_type_label(self):
        post = Post.objects.get(uuid = 'f02b44c7-c5db-4a20-9651-7a0658085ee8')
        field_label = post._meta.get_field('type').verbose_name
        self.assertEqual(field_label, 'type')
    
    def test_title_label(self):
        post = Post.objects.get(uuid = 'f02b44c7-c5db-4a20-9651-7a0658085ee8')
        field_label = post._meta.get_field('title').verbose_name
        self.assertEqual(field_label, 'title')

    def test_uuid_label(self):
        post = Post.objects.get(uuid = 'f02b44c7-c5db-4a20-9651-7a0658085ee8')
        field_label = post._meta.get_field('uuid').verbose_name
        self.assertEqual(field_label, 'uuid')

    def test_id_label(self):
        post = Post.objects.get(uuid = 'f02b44c7-c5db-4a20-9651-7a0658085ee8')
        field_label = post._meta.get_field('id').verbose_name
        self.assertEqual(field_label, 'id')

    def test_source_label(self):
        post = Post.objects.get(uuid = 'f02b44c7-c5db-4a20-9651-7a0658085ee8')
        field_label = post._meta.get_field('source').verbose_name
        self.assertEqual(field_label, 'source')

    def test_origin_label(self):
        post = Post.objects.get(uuid = 'f02b44c7-c5db-4a20-9651-7a0658085ee8')
        field_label = post._meta.get_field('origin').verbose_name
        self.assertEqual(field_label, 'origin')
    
    def test_description_label(self):
        post = Post.objects.get(uuid = 'f02b44c7-c5db-4a20-9651-7a0658085ee8')
        field_label = post._meta.get_field('description').verbose_name
        self.assertEqual(field_label, 'description')
    
    def test_contentType_label(self):
        post = Post.objects.get(uuid = 'f02b44c7-c5db-4a20-9651-7a0658085ee8')
        field_label = post._meta.get_field('contentType').verbose_name
        self.assertEqual(field_label, 'contentType')
    
    def test_content_label(self):
        post = Post.objects.get(uuid = 'f02b44c7-c5db-4a20-9651-7a0658085ee8')
        field_label = post._meta.get_field('content').verbose_name
        self.assertEqual(field_label, 'content')
    
    def test_author_label(self):
        post = Post.objects.get(uuid = 'f02b44c7-c5db-4a20-9651-7a0658085ee8')
        field_label = post._meta.get_field('author').verbose_name
        self.assertEqual(field_label, 'author')

    def test_categories_label(self):
        post = Post.objects.get(uuid = 'f02b44c7-c5db-4a20-9651-7a0658085ee8')
        field_label = post._meta.get_field('categories').verbose_name
        self.assertEqual(field_label, 'categories')

    def test_count_label(self):
        post = Post.objects.get(uuid = 'f02b44c7-c5db-4a20-9651-7a0658085ee8')
        field_label = post._meta.get_field('count').verbose_name
        self.assertEqual(field_label, 'count')

    def test_comments_label(self):
        post = Post.objects.get(uuid = 'f02b44c7-c5db-4a20-9651-7a0658085ee8')
        field_label = post._meta.get_field('comments').verbose_name
        self.assertEqual(field_label, 'comments')

    def test_published_label(self):
        post = Post.objects.get(uuid = 'f02b44c7-c5db-4a20-9651-7a0658085ee8')
        field_label = post._meta.get_field('published').verbose_name
        self.assertEqual(field_label, 'published')
    
    def test_visibility_label(self):
        post = Post.objects.get(uuid = 'f02b44c7-c5db-4a20-9651-7a0658085ee8')
        field_label = post._meta.get_field('visibility').verbose_name
        self.assertEqual(field_label, 'visibility')
    
    def test_unlisted_label(self):
        post = Post.objects.get(uuid = 'f02b44c7-c5db-4a20-9651-7a0658085ee8')
        field_label = post._meta.get_field('unlisted').verbose_name
        self.assertEqual(field_label, 'unlisted')
    
    def test_type_max_length(self):
        post = Post.objects.get(uuid = 'f02b44c7-c5db-4a20-9651-7a0658085ee8')
        max_length = post._meta.get_field('type').max_length
        self.assertEqual(max_length, 100)

    def test_title_max_length(self):
        post = Post.objects.get(uuid = 'f02b44c7-c5db-4a20-9651-7a0658085ee8')
        max_length = post._meta.get_field('title').max_length
        self.assertEqual(max_length, 100)
    
    def test_description_max_length(self):
        post = Post.objects.get(uuid = 'f02b44c7-c5db-4a20-9651-7a0658085ee8')
        max_length = post._meta.get_field('description').max_length
        self.assertEqual(max_length, 500)
    
    def test_contentType_max_length(self):
        post = Post.objects.get(uuid = 'f02b44c7-c5db-4a20-9651-7a0658085ee8')
        max_length = post._meta.get_field('contentType').max_length
        self.assertEqual(max_length, 20)

    def test_categories_max_length(self):
        post = Post.objects.get(uuid = 'f02b44c7-c5db-4a20-9651-7a0658085ee8')
        max_length = post._meta.get_field('categories').max_length
        self.assertEqual(max_length, 100)
    
    def test_visibility_max_length(self):
        post = Post.objects.get(uuid = 'f02b44c7-c5db-4a20-9651-7a0658085ee8')
        max_length = post._meta.get_field('visibility').max_length
        self.assertEqual(max_length, 10)


# class Comment(models.Model):
#     CONTENTCHOICES = (
#         ("text/plain", "Plain"),
#         ("text/markdown", "Markdown")
#     )

#     uuid = models.UUIDField(primary_key=True, null=False, default=uuid.uuid4, editable=False)
#     id = models.URLField(null=True)
#     type = models.CharField(default='comment', max_length=50)
#     author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='comment_author')
#     post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comment_post')
#     comment = models.CharField(max_length=1024)
#     contentType = models.CharField(max_length=18, choices=CONTENTCHOICES, default="text/plain")
#     published = models.DateTimeField(null=True, auto_now_add=True)



