from django.test import TestCase
from django.utils import unittest
from post.models import Post, VisibleToAuthor, PostImage
from django.contrib.auth.models import AnonymousUser, User
from django.test.utils import setup_test_environment
from django.test.client import Client
from django.test import TestCase
from django.test import Client
from django.contrib.auth.models import User
from author.models import Author
from django.core.files import File
from images.models import Image

# Create your tests here.


class Post_testcase(TestCase):

    def setUp(self):
        setup_test_environment()
        user1 = User.objects.create_user(username="myuser1",
                                         password="mypassword")
        user2 = User.objects.create_user(username="myuser2",
                                         password="mypassword")
        user3 = User.objects.create_user(username="results1",
                                         password="mypassword")
        user4 = User.objects.create_user(username="results2",
                                         password="mypassword")
        author1 = Author.objects.create(user=user1, github_user='mygithubuser')
        author2 = Author.objects.create(user=user2, github_user='mygithubuser')
        author3 = Author.objects.create(user=user3, github_user='mygithubuser')
        author4 = Author.objects.create(user=user4, github_user='mygithubuser')
        # user1 = Post.objects.create(title="1",description="aaa",guid="",content="aaa",content_type="PLAIN_TEXT",visibility="PUBLIC",author="1")

    def test_creating_post(self):
        c = Client()
        response = c.post('/author/posts/create_post', {'title': '1',
                                                        'description': 'aaaa',
                                                        'text_body': '1231',
                                                        'user': 'myuser1'})
        self.assertEqual(response.status_code, 301)

    def test_delete_post(self):
        c = Client()
        response = c.delete('/author/posts/create_post', {'title': '1',
                                                          'description': 'aaaa',
                                                          'text_body': '1231',
                                                          'user': 'myuser1'})
        self.assertEqual(response.status_code, 301)

    def test_invaild_missing_user(self):
        c = Client()
        response = c.post('/author/posts/create_post', {'title': '2', 'description': 'bbbb',
                                                        'text_body': '121',
                                                        })
        self.assertEqual(response.status_code, 301)

    def test_comments(self):
        c = Client()
        response = c.post('/author/posts/create_post', {'title': '2', 'description': 'cccc',
                                                        'text_body': '121',
                                                        'comments': 'comments'
                                                        })
        self.assertEqual(response.status_code, 301)

    def test_logout_redirect(self):
        c = Client()
        response = c.get('/author/logout')
        self.assertEqual(response.status_code, 301)

    def test_profile_redirect(self):
        c = Client()
        response = c.get('/author/myuser1')
        self.assertEqual(response.status_code, 301)

    def test_friends_request_redirect(self):
        c = Client()
        c.login(username='myuser1', password='mypassword')
        user1 = User.objects.get(username="myuser1")
        url = '/author/' + str(user1.id) + '/FriendRequests'
        response = c.get(url)
        self.assertEqual(response.status_code, 200)

    def test_image_redirect(self):
        c = Client()
        response = c.get('/images/uploadImage')
        self.assertEqual(response.status_code, 301)

    def test_is_pravite(self):
        c = Client()
        response = c.post('/author/posts/create_post', {'title': '2', 'description': 'dddd',
                                                        'text_body': '121',
                                                        'visibility': 'PRIVATE',
                                                        'author': 'myuser1'
                                                        })
        response2 = c.get('/author/posts/create_post', {'title': '2', 'description': 'ffff',
                                                        'text_body': '121',
                                                        'visibility': 'PRIVATE',
                                                        'author': 'myuser1'
                                                        })

        self.assertNotEqual(response, response2)


class Test_image(TestCase):

    def test_upload(self):
        i1 = Image()
        i1.title = "aaa"
        i1.thumb = File(open("static/images/comments4.png"))
        i1.save()

        p = Image.objects.get(id=1).thumb.path

        self.failUnless(open(p), 'file not found')
