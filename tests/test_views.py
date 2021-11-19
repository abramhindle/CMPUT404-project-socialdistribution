import json
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from http import HTTPStatus
from backend.serializers import AuthorSerializer, CommentSerializer, PostSerializer, LikeSerializer

from backend.models import Author, Post, Like, Comment
import requests
from datetime import datetime
from django.utils.dateparse import parse_datetime
import uuid


class AuthorListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        number_of_authors = 5
        User.objects.bulk_create([
            User(username="AuthorListViewTest_{}".format(idx),
            password=make_password("Margret Thatcher"),
            is_active=True
            ) for idx in range(number_of_authors)
        ])
        for author_id in range(number_of_authors):
            Author.objects.create(
                user=User.objects.get(username="AuthorListViewTest_{}".format(author_id)),
                display_name="Test unit{}".format(author_id),
            )

    def test_view_url_exists_at_desired_location(self):
        res = self.client.get("/api/authors/")
        self.assertEqual(res.status_code, 200)

    def test_correct_number_of_authors(self):
        res = self.client.get("/api/authors/")
        self.assertEqual(res.status_code, 200)
        body = json.loads(res.content.decode("utf-8"))
        self.assertEqual(len(body["items"]), 5)

class AuthorViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        uuid_list = [
            "95a1e643-180c-4de6-8fc5-9cb48a216fbe",
            "856c692d-2514-4d06-80fc-4c4312188db3",
            "bf453da8-459c-4064-a6bc-21d8f24c6d7f",
            "4d5baaf2-0cc5-4fd0-89a7-21ddc46e6e2e",
            "b3c492b6-a690-4b89-b2c1-23d21433fdce",
        ]
        number_of_authors = len(uuid_list)
        User.objects.bulk_create([
            User(username="AuthorViewTest_{}".format(idx),
            password=make_password("Margret Thatcher"),
            is_active=True
            ) for idx in range(number_of_authors)
        ])
        for author_id in range(number_of_authors):
            Author.objects.create(
                id=uuid_list[author_id],
                user=User.objects.get(username="AuthorViewTest_{}".format(author_id)),
                display_name="Test unit{}".format(author_id),
            )
    def test_author_not_found(self):
        res = self.client.get("/api/author/282848/")
        self.assertEqual(res.status_code, 404)

    def test_valid_author_profile(self):
        res = self.client.get("/api/author/b3c492b6-a690-4b89-b2c1-23d21433fdce/")
        self.assertEqual(res.status_code, 200)
        

class SignupViewTest(TestCase):
    def test_get(self):
        res = self.client.get("/api/signup/")

        self.assertEqual(res.status_code, HTTPStatus.OK)

    def test_post(self):
        data = {
            'username':'test',
            'display_name': 'test',
            'password1': 'margaret thatcher',
            'password2': 'margaret thatcher',
        }
        res = self.client.post("/api/signup/", data = data)
        self.assertEqual(res.status_code, HTTPStatus.OK)

class LoginViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        uuid_list = [
            "95a1e643-180c-4de6-8fc5-9cb48a216fbe",
            "856c692d-2514-4d06-80fc-4c4312188db3",
            "bf453da8-459c-4064-a6bc-21d8f24c6d7f",
        ]
        number_of_authors = len(uuid_list)
        User.objects.bulk_create([
            User(username="LoginViewTest{}".format(idx),
            password=make_password("Margret Thatcher"),
            is_active = False if idx == 2 else True
            ) for idx in range(number_of_authors)
        ])
        for author_id in range(number_of_authors):
            Author.objects.create(
                id=uuid_list[author_id],
                user=User.objects.get(username="LoginViewTest{}".format(author_id)),
                display_name="Test unit{}".format(author_id),
                url="http://127.0.0.1:8000/author/{}".format(uuid_list[author_id]),
                host="http://127.0.0.1:8000/",
            )
    def test_get_not_allowed(self):
        res = self.client.get("/api/login/")

        self.assertEqual(res.status_code, HTTPStatus.METHOD_NOT_ALLOWED)

    def test_valid_login(self):
        data = {
            "username": "LoginViewTest0",
            "password":"Margret Thatcher"
        }
        res = self.client.post("/api/login/", data=data, follow=True)
        self.assertEqual(res.status_code, HTTPStatus.OK)
        
    def test_invalid_login(self):
        data = {
            "username": "asdf",
            "password":"asdf"
        }
        res = self.client.post("/api/login/", data=data, content_type="application/json")
        self.assertEqual(res.status_code, HTTPStatus.BAD_REQUEST)

    def test_non_active_login(self):
        data = {
            "username": "LoginViewTest2",
            "password":"Margret Thatcher"
        }
        res = self.client.post("/api/login/", data=data)
        self.assertEqual(res.status_code, HTTPStatus.BAD_REQUEST)
        

class PostViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        uuid_list = [
            "2f91a911-850f-4655-ac29-9115822c72b5",
            "2f91a911-850f-4655-ac29-9115822c72b6",
            "2f91a911-850f-4655-ac29-9115822c72b7",
        ]
        number_of_authors = len(uuid_list)
        User.objects.bulk_create([
            User(username="LoginViewTest{}".format(idx),
            password=make_password("Margret Thatcher"),
            is_active = False if idx == 2 else True
            ) for idx in range(number_of_authors)
        ])
        authors = []
        for author_id in range(number_of_authors):
                authors.append(Author.objects.create(
                id=uuid_list[author_id],
                user=User.objects.get(username="LoginViewTest{}".format(author_id)),
                display_name="Test unit{}".format(author_id),
                url="http://127.0.0.1:8000/author/{}".format(uuid_list[author_id]),
                host="http://127.0.0.1:8000/",
            ))
        post = Post.objects.create(
            id="2f91a911-850f-4655-ac29-9115822c72a9",
            url="http://127.0.0.1:8000/author/2f91a911-850f-4655-ac29-9115822c72b5/post/2f91a911-850f-4655-ac29-9115822c72a9",
            title="Test Title",
            source = "https://www.youtube.com/watch?v=YIJI5U0BWr0",
            origin = "https://www.django-rest-framework.org/api-guide/views/",
            description = "Test Post",
            content_type = "text/plain",
            published="2015-03-09T13:07:04+00:00",
            content = "test text",
            author = authors[0],
        )
    def test_author_not_found(self):
        res = self.client.get("/api/author/2f91a911-850f-4655-ac2FAKE-9115822c72b5/posts/2f91a911-850f-4655-ac29-9115822c72c9/")
        self.assertEqual(res.status_code, 404)

    def test_post_not_found(self):
        res = self.client.get("/api/author/2f91a911-850f-4655-ac29-9115822c72b5/posts/2f91a911-850f-4655-ac29-9115822c72c9/")
        self.assertEqual(res.status_code, 404)

    def test_valid_post(self):
        res = self.client.get("/api/author/2f91a911-850f-4655-ac29-9115822c72b5/posts/2f91a911-850f-4655-ac29-9115822c72a9")
        #https://stackoverflow.com/questions/16877422/whats-the-best-way-to-parse-a-json-response-from-the-requests-library
        res_content = json.loads(res.content)
        self.assertEqual(res_content["id"], "http://127.0.0.1:8000/author/2f91a911-850f-4655-ac29-9115822c72b5/post/2f91a911-850f-4655-ac29-9115822c72a9")
    def test_post_post(self):
        post_data = {
            "title":'New Title',
            "source":"https://www.geeksforgeeks.org/python-unittest-assertnotequal-function/",
            "origin":"https://www.geeksforgeeks.org/python-unittest-assertnotequal-function/",
            "description":"yee",
            "content_type":"text/plain",
            "published":"2015-03-09T13:07:04+00:00",
            "visibility":"PUBLIC",
            "unlisted":False
        }
        post_res = self.client.post("/api/author/2f91a911-850f-4655-ac29-9115822c72b5/posts/2f91a911-850f-4655-ac29-9115822c72a9",data=post_data,follow=True,content_type="application/json")
        get_res = self.client.get("/api/author/2f91a911-850f-4655-ac29-9115822c72b5/posts/2f91a911-850f-4655-ac29-9115822c72a9")
        get_res_content = json.loads(get_res.content)
        self.assertEqual(get_res_content["title"], "New Title")
    def test_post_put(self):
        author=Author.objects.get(id="2f91a911-850f-4655-ac29-9115822c72b7")
        self.assertEqual(0,len(author.posted.all()))
        author_serializer = AuthorSerializer(author)
        author_dict = author_serializer.data
        put_data = {
            "title":"Brand New Title",
            "source" : "https://www.youtube.com/watch?v=YIJI5U0BWr0",
            "origin" : "https://www.django-rest-framework.org/api-guide/views/",
            "description" : "Test Post",
            "content_type" : "text/plain",
            "content" : "test text",
            "author" : author_dict
        }
        put_res = self.client.put("/api/author/2f91a911-850f-4655-ac29-9115822c72b7/posts/2f91a911-850f-4655-ac29-9115822c72d9",data=put_data,follow=True,content_type="application/json")
        
        
        self.assertEqual(put_res.status_code, 201)
        self.assertEqual(1,len(author.posted.all()))
    def test_post_delete(self):
        author=Author.objects.get(id="2f91a911-850f-4655-ac29-9115822c72b5")
        self.assertEqual(1,len(author.posted.all()))
        put_res = self.client.delete("/api/author/2f91a911-850f-4655-ac29-9115822c72b5/posts/2f91a911-850f-4655-ac29-9115822c72a9",follow=True)
        self.assertEqual(0,len(author.posted.all()))

class PostListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        uuid_list = [
            "2f91a911-850f-4655-ac29-9115822c72b5",
            "2f91a911-850f-4655-ac29-9115822c72b6",
            "2f91a911-850f-4655-ac29-9115822c72b7",
        ]
        number_of_authors = len(uuid_list)
        User.objects.bulk_create([
            User(username="LoginViewTest{}".format(idx),
            password=make_password("Margret Thatcher"),
            is_active = False if idx == 2 else True
            ) for idx in range(number_of_authors)
        ])
        authors = []
        for author_id in range(number_of_authors):
                authors.append(Author.objects.create(
                id=uuid_list[author_id],
                user=User.objects.get(username="LoginViewTest{}".format(author_id)),
                display_name="Test unit{}".format(author_id),
                url="http://127.0.0.1:8000/author/{}".format(uuid_list[author_id]),
                host="http://127.0.0.1:8000/",
            ))
        post = Post.objects.create(
            id="2f91a911-850f-4655-ac29-9115822c72a9",
            url="http://127.0.0.1:8000/author/2f91a911-850f-4655-ac29-9115822c72b5/post/2f91a911-850f-4655-ac29-9115822c72a9",
            title="Test Title",
            source = "https://www.youtube.com/watch?v=YIJI5U0BWr0",
            origin = "https://www.django-rest-framework.org/api-guide/views/",
            description = "Test Post",
            content_type = "text/plain",
            published="2015-03-09T13:07:04+00:00",
            content = "test text",
            author = authors[0],
        )
        post = Post.objects.create(
            id="2f91a911-850f-4655-ac29-9115822c72a1",
            url="http://127.0.0.1:8000/author/2f91a911-850f-4655-ac29-9115822c72b5/post/2f91a911-850f-4655-ac29-9115822c72a1",
            title="Test Title2",
            source = "https://www.youtube.com/watch?v=YIJI5U0BWr0",
            origin = "https://www.django-rest-framework.org/api-guide/views/",
            description = "Test Post2",
            content_type = "text/plain",
            published="2015-03-09T13:07:04+00:00",
            content = "test text2",
            author = authors[0],
        )
        post = Post.objects.create(
            id="2f91a911-850f-4655-ac29-9115822c72b1",
            url="http://127.0.0.1:8000/author/2f91a911-850f-4655-ac29-9115822c72b6/post/2f91a911-850f-4655-ac29-9115822c72b1",
            title="Test Title2",
            source = "https://www.youtube.com/watch?v=YIJI5U0BWr0",
            origin = "https://www.django-rest-framework.org/api-guide/views/",
            description = "Test Post3",
            content_type = "text/plain",
            published="2015-03-09T13:07:04+00:00",
            content = "test text3",
            author = authors[1],
        )
    def test_author_not_found(self):
        res = self.client.get("/api/author/2f91a911-850f-4655-ac2FAKE-9115822c72b5/posts/2f91a911-850f-4655-ac29-9115822c72c9/")
        self.assertEqual(res.status_code, 404)

    def test_valid_posts(self):
        res = self.client.get("/api/author/2f91a911-850f-4655-ac29-9115822c72b5/posts/")
        res_content = json.loads(res.content)
        self.assertEqual(2,len(res_content["items"]))
    def test_posts_post(self):
        author=Author.objects.get(id="2f91a911-850f-4655-ac29-9115822c72b7")
        self.assertEqual(0,len(author.posted.all()))
        author_serializer = AuthorSerializer(author)
        author_dict = author_serializer.data
        post_data = {
            "title":'New Title',
            "source":"https://www.geeksforgeeks.org/python-unittest-assertnotequal-function/",
            "origin":"https://www.geeksforgeeks.org/python-unittest-assertnotequal-function/",
            "description":"yee",
            "content_type":"text/plain",
            "published":"2015-03-09T13:07:04+00:00",
            "visibility":"PUBLIC",
            "unlisted":False,
            "author": author_dict
        }
        post_res = self.client.post("/api/author/2f91a911-850f-4655-ac29-9115822c72b7/posts/",data=post_data,follow=True,content_type="application/json")
        self.assertEqual(post_res.status_code, 201)
        self.assertEqual(1,len(author.posted.all()))
    def test_all_posts_get(self):
        res = self.client.get("/api/posts/")
        res_content = json.loads(res.content)
        self.assertEqual(3,len(res_content["items"]))

class CommentViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        uuid_list = [
            "2f91a911-850f-4655-ac29-9115822c72a8",
            "2f91a911-850f-4655-ac29-9115822c72a6",
        ]
        number_of_authors = len(uuid_list)
        User.objects.bulk_create([
            User(username="LoginViewTest{}".format(idx),
            password=make_password("Margret Thatcher"),
            is_active = False if idx == 2 else True
            ) for idx in range(number_of_authors)
        ])
        authors = []
        for author_id in range(number_of_authors):
                authors.append(Author.objects.create(
                id=uuid_list[author_id],
                user=User.objects.get(username="LoginViewTest{}".format(author_id)),
                display_name="Test unit{}".format(author_id),
                url="http://127.0.0.1:8000/author/{}".format(uuid_list[author_id]),
                host="http://127.0.0.1:8000/",
            ))
        post = Post.objects.create(
            id="2f91a911-850f-4655-ac29-9115822c72a9",
            url="http://127.0.0.1:8000/author/2f91a911-850f-4655-ac29-9115822c72a8/post/2f91a911-850f-4655-ac29-9115822c72a9",
            title="Test Title",
            source = "https://www.youtube.com/watch?v=YIJI5U0BWr0",
            origin = "https://www.django-rest-framework.org/api-guide/views/",
            description = "Test Post",
            content_type = "text/plain",
            content = "test text",
            author = authors[0],
        )
        Comment.objects.create(
            id="2f91a911-850f-4655-ac29-9115822c72a7",
            url="http://127.0.0.1:8000/author/2f91a911-850f-4655-ac29-9115822c72a8/post/2f91a911-850f-4655-ac29-9115822c72a9/comment/2f91a911-850f-4655-ac29-9115822c72a7",
            post = post,
            author = authors[1],
            comment = "This is a test comment",
        )
        Comment.objects.create(
            id="2f91a911-850f-4655-ac29-9115822c72b7",
            url="http://127.0.0.1:8000/author/2f91a911-850f-4655-ac29-9115822c72a8/post/2f91a911-850f-4655-ac29-9115822c72a9/comment/2f91a911-850f-4655-ac29-9115822c72b7",
            post = post,
            author = authors[1],
            comment = "This is a test comment2",
        )
    def test_author_not_found(self):
        res = self.client.get("/api/author/2f91a911-850f-4655-ac2FAKE-9115822c72b5/posts/2f91a911-850f-4655-ac29-9115822c72a9/")
        self.assertEqual(res.status_code, 404)

    def test_post_not_found(self):
        res = self.client.get("/api/author/2f91a911-850f-4655-ac29-9115822c72a8/posts/2f91a911FAKE-850f-4655-ac29-9115822c72a9/")
        self.assertEqual(res.status_code, 404)

    def test_valid_comments_get(self):
        res = self.client.get("/api/author/2f91a911-850f-4655-ac29-9115822c72a8/posts/2f91a911-850f-4655-ac29-9115822c72a9/comments")
        res_content = json.loads(res.content)
        self.assertEqual(2,len(res_content["items"]))
        #self.assertEqual(res_content["items"][0]["id"],"http://127.0.0.1:8000/comment/2f91a911-850f-4655-ac29-9115822c72a7")
    def test_valid_comments_post(self):
        res = self.client.get("/api/author/2f91a911-850f-4655-ac29-9115822c72a8/posts/2f91a911-850f-4655-ac29-9115822c72a9/comments")
        res_content = json.loads(res.content)
        self.assertEqual(2,len(res_content["items"]))

class FollowersListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        uuid_list = [
            "2f91a911-850f-4655-ac29-9115822c72a8",
            "2f91a911-850f-4655-ac29-9115822c72a6",
            "2f91a911-850f-4655-ac29-9115822c72a4",
            "2f91a911-850f-4655-ac29-9115822c72a2",
        ]
        number_of_authors = len(uuid_list)
        User.objects.bulk_create([
            User(username="LoginViewTest{}".format(idx),
            password=make_password("Margret Thatcher"),
            is_active = False if idx == 2 else True
            ) for idx in range(number_of_authors)
        ])
        authors = []
        for author_id in range(number_of_authors):
                authors.append(Author.objects.create(
                id=uuid_list[author_id],
                user=User.objects.get(username="LoginViewTest{}".format(author_id)),
                display_name="Test unit{}".format(author_id),
                url="http://127.0.0.1:8000/author/{}".format(uuid_list[author_id]),
                host="http://127.0.0.1:8000/",
                ))
        #https://stackoverflow.com/questions/17826629/how-to-set-value-of-a-manytomany-field-in-django
        authors[0].followers.add(Author.objects.get(id = "2f91a911-850f-4655-ac29-9115822c72a6"))
        authors[0].followers.add(Author.objects.get(id = "2f91a911-850f-4655-ac29-9115822c72a2"))

    def test_author_not_found(self):
        res = self.client.get("/api/author/2f91a911-850f-4655-ac2FAKE-9115822c72b5/followers/")
        self.assertEqual(res.status_code, 404)
    def test_followers(self):
        res = self.client.get("/api/author/2f91a911-850f-4655-ac29-9115822c72a8/followers")
        body = json.loads(res.content.decode("utf-8"))
        self.assertEqual(len(body["items"]), 2)

class FollowersViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        uuid_list = [
            "2f91a911-850f-4655-ac29-9115822c72a8",
            "2f91a911-850f-4655-ac29-9115822c72a6",
            "2f91a911-850f-4655-ac29-9115822c72a4",
            "2f91a911-850f-4655-ac29-9115822c72a2",
        ]
        number_of_authors = len(uuid_list)
        User.objects.bulk_create([
            User(username="LoginViewTest{}".format(idx),
            password=make_password("Margret Thatcher"),
            is_active = False if idx == 2 else True
            ) for idx in range(number_of_authors)
        ])
        authors = []
        for author_id in range(number_of_authors):
                authors.append(Author.objects.create(
                id=uuid_list[author_id],
                user=User.objects.get(username="LoginViewTest{}".format(author_id)),
                display_name="Test unit{}".format(author_id),
                url="http://127.0.0.1:8000/author/{}".format(uuid_list[author_id]),
                host="http://127.0.0.1:8000/",
                ))
        #https://stackoverflow.com/questions/17826629/how-to-set-value-of-a-manytomany-field-in-django
        authors[0].followers.add(Author.objects.get(id = "2f91a911-850f-4655-ac29-9115822c72a6"))
        authors[0].followers.add(Author.objects.get(id = "2f91a911-850f-4655-ac29-9115822c72a2"))

    def test_foreign_author_not_found(self):
        res = self.client.get("/api/author/2f91a911-850f-4655-ac29-9115822c72a8/followers/2f91a911-FAKE850f-4655-ac29-9115822c72a6")
        self.assertEqual(res.status_code, 404)
    def test_get_valid_follower(self):
        res = self.client.get("/api/author/2f91a911-850f-4655-ac29-9115822c72a8/followers/2f91a911-850f-4655-ac29-9115822c72a2")
        self.assertEqual(res.status_code, 200)
    def test_get_valid_non_follower(self):
        res = self.client.get("/api/author/2f91a911-850f-4655-ac29-9115822c72a8/followers/2f91a911-850f-4655-ac29-9115822c72a4")
        self.assertEqual(res.status_code, 404)
    def test_followers_put(self):
        author=Author.objects.get(id="2f91a911-850f-4655-ac29-9115822c72a8")
        self.assertEqual(2,len(author.followers.all()))
        put_res = self.client.put("/api/author/2f91a911-850f-4655-ac29-9115822c72a8/followers/2f91a911-850f-4655-ac29-9115822c72a4",data={},follow=True,content_type="application/json")
        self.assertEqual(3,len(author.followers.all()))
    def test_followers_put_invalid_author(self):
        put_res = self.client.put("/api/author/2f91a911-850f-4655-ac29-9115822c72a8/followers/2f91a911-FAKE850f-4655-ac29-9115822c72a4",data={},follow=True,content_type="application/json")
        self.assertEqual(put_res.status_code, 404)
    def test_followers_delete(self):
        author=Author.objects.get(id="2f91a911-850f-4655-ac29-9115822c72a8")
        self.assertEqual(2,len(author.followers.all()))
        put_res = self.client.delete("/api/author/2f91a911-850f-4655-ac29-9115822c72a8/followers/2f91a911-850f-4655-ac29-9115822c72a6",data={},follow=True,content_type="application/json")
        self.assertEqual(1,len(author.followers.all()))
    def test_followers_delete_invalid_author(self):
        delete_res = self.client.delete("/api/author/2f91a911-850f-4655-ac29-9115822c72a8/followers/2f91a911-850f-4655-ac29-FAKE9115822c72a4",data={},follow=True,content_type="application/json")
        self.assertEqual(delete_res.status_code, 404)
    def test_followers_delete_non_follower(self):
        delete_res = self.client.delete("/api/author/2f91a911-850f-4655-ac29-9115822c72a8/followers/2f91a911-850f-4655-ac29-9115822c72a4",data={},follow=True,content_type="application/json")
        self.assertEqual(delete_res.status_code, 404)

class FriendsViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        uuid_list = [
            "2f91a911-850f-4655-ac29-9115822c72a8",
            "2f91a911-850f-4655-ac29-9115822c72a6",
            "2f91a911-850f-4655-ac29-9115822c72a4",
            "2f91a911-850f-4655-ac29-9115822c72a2",
        ]
        number_of_authors = len(uuid_list)
        User.objects.bulk_create([
            User(username="LoginViewTest{}".format(idx),
            password=make_password("Margret Thatcher"),
            is_active = False if idx == 2 else True
            ) for idx in range(number_of_authors)
        ])
        authors = []
        for author_id in range(number_of_authors):
                authors.append(Author.objects.create(
                id=uuid_list[author_id],
                user=User.objects.get(username="LoginViewTest{}".format(author_id)),
                display_name="Test unit{}".format(author_id),
                url="http://127.0.0.1:8000/author/{}".format(uuid_list[author_id]),
                host="http://127.0.0.1:8000/",
                ))
        #https://stackoverflow.com/questions/17826629/how-to-set-value-of-a-manytomany-field-in-django
        authors[0].followers.add(Author.objects.get(id = "2f91a911-850f-4655-ac29-9115822c72a6"))
        authors[1].followers.add(Author.objects.get(id = "2f91a911-850f-4655-ac29-9115822c72a8"))
        authors[2].followers.add(Author.objects.get(id = "2f91a911-850f-4655-ac29-9115822c72a8"))
        authors[0].followers.add(Author.objects.get(id = "2f91a911-850f-4655-ac29-9115822c72a2"))

    def test_author_not_found(self):
        res = self.client.get("/api/author/2f91a911-850f-4655-ac2FAKE-9115822c72b5/friends/")
        self.assertEqual(res.status_code, 404)
    def test_friends(self):
        res = self.client.get("/api/author/2f91a911-850f-4655-ac29-9115822c72a8/friends")
        body = json.loads(res.content.decode("utf-8"))
        self.assertEqual(len(body["items"]), 1)
    def test_following_different_than_friends(self):
        res = self.client.get("/api/author/2f91a911-850f-4655-ac29-9115822c72a4/friends")
        body = json.loads(res.content.decode("utf-8"))
        self.assertEqual(len(body["items"]), 0)
        res = self.client.get("/api/author/2f91a911-850f-4655-ac29-9115822c72a2/friends")
        body = json.loads(res.content.decode("utf-8"))
        self.assertEqual(len(body["items"]), 0)
    def test_invalid_friend(self):
        res = self.client.get("/api/author/2f91a911-850f-4655-ac29-9115822c72a4/friends/FAKE2f91a911-850f-4655-ac29-9115822c72a6")
        self.assertEqual(res.status_code, 404)
    def test_valid_friend(self):
        res = self.client.get("/api/author/2f91a911-850f-4655-ac29-9115822c72a8/friends/2f91a911-850f-4655-ac29-9115822c72a6")
        body = json.loads(res.content.decode("utf-8"))
        self.assertEqual(body["id"], "http://127.0.0.1:8000/author/2f91a911-850f-4655-ac29-9115822c72a6")

class LikedViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        uuid_list = [
            "2f91a911-850f-4655-ac29-9115822c72b5",
            "2f91a911-850f-4655-ac29-9115822c72b6",
            "2f91a911-850f-4655-ac29-9115822c72b7",
        ]
        number_of_authors = len(uuid_list)
        User.objects.bulk_create([
            User(username="LoginViewTest{}".format(idx),
            password=make_password("Margret Thatcher"),
            is_active = False if idx == 2 else True
            ) for idx in range(number_of_authors)
        ])
        authors = []
        for author_id in range(number_of_authors):
                authors.append(Author.objects.create(
                id=uuid_list[author_id],
                user=User.objects.get(username="LoginViewTest{}".format(author_id)),
                display_name="Test unit{}".format(author_id),
                url="http://127.0.0.1:8000/author/{}".format(uuid_list[author_id]),
                host="http://127.0.0.1:8000/",
            ))
        post = Post.objects.create(
            id="2f91a911-850f-4655-ac29-9115822c72a9",
            url="http://127.0.0.1:8000/author/2f91a911-850f-4655-ac29-9115822c72b5/post/2f91a911-850f-4655-ac29-9115822c72a9",
            title="Test Title",
            source = "https://www.youtube.com/watch?v=YIJI5U0BWr0",
            origin = "https://www.django-rest-framework.org/api-guide/views/",
            description = "Test Post",
            content_type = "text/plain",
            content = "test text",
            author = authors[0],
        )
        post_like = Like.objects.create(
            object="http://127.0.0.1:8000/author/2f91a911-850f-4655-ac29-9115822c72b5/post/2f91a911-850f-4655-ac29-9115822c72a9",
            author = authors[1],
            summary = "liking author likes post",
        )
        comment= Comment.objects.create(
            id="2f91a911-850f-4655-ac29-9115822c72a7",
            url="http://127.0.0.1:8000/author/2f91a911-850f-4655-ac29-9115822c72b5/post/2f91a911-850f-4655-ac29-9115822c72a9/comment/2f91a911-850f-4655-ac29-9115822c72a7",
            post = post,
            author = authors[2],
            comment = "This is a test comment",
        )
        comment_like = Like.objects.create(
            object="http://127.0.0.1:8000/author/2f91a911-850f-4655-ac29-9115822c72b5/post/2f91a911-850f-4655-ac29-9115822c72a9/comment/2f91a911-850f-4655-ac29-9115822c72a7",
            author = authors[1],
            summary = "liking author likes post",
        )
    def test_author_not_found(self):
        res = self.client.get("/api/author/282848/liked/")
        self.assertEqual(res.status_code, 404)

    def test_valid_post_liked_and_comment_liked(self):
        res = self.client.get("/api/author/2f91a911-850f-4655-ac29-9115822c72b6/liked")
        body = json.loads(res.content.decode("utf-8"))
        self.assertEqual(len(body["items"]), 2)
        self.assertEqual(res.status_code, 200)

class LikesViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        uuid_list = [
            "2f91a911-850f-4655-ac29-9115822c72b5",
            "2f91a911-850f-4655-ac29-9115822c72b6",
            "2f91a911-850f-4655-ac29-9115822c72b7",
            "2f91a911-850f-4655-ac29-9115822c72b9"
        ]
        number_of_authors = len(uuid_list)
        User.objects.bulk_create([
            User(username="LoginViewTest{}".format(idx),
            password=make_password("Margret Thatcher"),
            is_active = False if idx == 2 else True
            ) for idx in range(number_of_authors)
        ])
        authors = []
        for author_id in range(number_of_authors):
                authors.append(Author.objects.create(
                id=uuid_list[author_id],
                user=User.objects.get(username="LoginViewTest{}".format(author_id)),
                display_name="Test unit{}".format(author_id),
                url="http://127.0.0.1:8000/author/{}".format(uuid_list[author_id]),
                host="http://127.0.0.1:8000/",
            ))
        post = Post.objects.create(
            id="2f91a911-850f-4655-ac29-9115822c72a9",
            url="http://127.0.0.1:8000/author/2f91a911-850f-4655-ac29-9115822c72b5/post/2f91a911-850f-4655-ac29-9115822c72a9",
            title="Test Title",
            source = "https://www.youtube.com/watch?v=YIJI5U0BWr0",
            origin = "https://www.django-rest-framework.org/api-guide/views/",
            description = "Test Post",
            content_type = "text/plain",
            content = "test text",
            author = authors[0],
        )
        post_like = Like.objects.create(
            object="http://127.0.0.1:8000/author/2f91a911-850f-4655-ac29-9115822c72b5/post/2f91a911-850f-4655-ac29-9115822c72a9",
            author = authors[1],
            summary = "liking author likes post",
        )
        comment= Comment.objects.create(
            id="2f91a911-850f-4655-ac29-9115822c72a7",
            url="http://127.0.0.1:8000/author/2f91a911-850f-4655-ac29-9115822c72b5/post/2f91a911-850f-4655-ac29-9115822c72a9/comment/2f91a911-850f-4655-ac29-9115822c72a7",
            post = post,
            author = authors[2],
            comment = "This is a test comment",
        )
        comment_like = Like.objects.create(
            object="http://127.0.0.1:8000/author/2f91a911-850f-4655-ac29-9115822c72b5/post/2f91a911-850f-4655-ac29-9115822c72a9/comment/2f91a911-850f-4655-ac29-9115822c72a7",
            author = authors[1],
            summary = "liking author likes post",
        )
    def test_author_not_found(self):
        res = self.client.get("/api/author/282848/liked")
        self.assertEqual(res.status_code, 404)

    def test_valid_post_likes(self):
        res = self.client.get("/api/author/2f91a911-850f-4655-ac29-9115822c72b5/post/2f91a911-850f-4655-ac29-9115822c72a9/likes")
        body = json.loads(res.content.decode("utf-8"))
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(body["items"]), 1)
    
    def test_valid_comment_likes(self):
        res = self.client.get("/api/author/2f91a911-850f-4655-ac29-9115822c72b5/post/2f91a911-850f-4655-ac29-9115822c72a9/comment/2f91a911-850f-4655-ac29-9115822c72a7/likes")
        body = json.loads(res.content.decode("utf-8"))
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(body["items"]), 1)

    def test_post_post_like(self):
        res = self.client.get("/api/author/2f91a911-850f-4655-ac29-9115822c72b5/post/2f91a911-850f-4655-ac29-9115822c72a9/likes")
        body = json.loads(res.content.decode("utf-8"))
        self.assertEqual(len(body["items"]), 1)

        author=Author.objects.get(id="2f91a911-850f-4655-ac29-9115822c72b9")
        author_serializer = AuthorSerializer(author)
        author_dict = author_serializer.data
        post_data = {
            "summary": "Lara Croft Likes your post",
            "type": "Like",
            "object":"http://127.0.0.1:8000/author/2f91a911-850f-4655-ac29-9115822c72b5/post/2f91a911-850f-4655-ac29-9115822c72a9",
            "author" : author_dict,
        }
        post_res = self.client.post("/api/author/2f91a911-850f-4655-ac29-9115822c72b5/inbox/",data=post_data,follow=True,content_type="application/json")
        self.assertEqual(post_res.status_code,200)

        res = self.client.get("/api/author/2f91a911-850f-4655-ac29-9115822c72b5/post/2f91a911-850f-4655-ac29-9115822c72a9/likes")
        body = json.loads(res.content.decode("utf-8"))
        self.assertEqual(len(body["items"]), 2)

    def test_comment_post_like(self):
        res = self.client.get("/api/author/2f91a911-850f-4655-ac29-9115822c72b5/post/2f91a911-850f-4655-ac29-9115822c72a9/comment/2f91a911-850f-4655-ac29-9115822c72a7/likes")
        body = json.loads(res.content.decode("utf-8"))
        self.assertEqual(len(body["items"]), 1)

        author=Author.objects.get(id="2f91a911-850f-4655-ac29-9115822c72b9")
        author_serializer = AuthorSerializer(author)
        author_dict = author_serializer.data
        post_data = {
            "summary": "Lara Croft Likes your post",
            "type": "Like",
            "object":"http://127.0.0.1:8000/author/2f91a911-850f-4655-ac29-9115822c72b5/post/2f91a911-850f-4655-ac29-9115822c72a9/comment/2f91a911-850f-4655-ac29-9115822c72a7",
            "author" : author_dict,
        }
        post_res = self.client.post("/api/author/2f91a911-850f-4655-ac29-9115822c72b5/inbox/",data=post_data,follow=True,content_type="application/json")
        self.assertEqual(post_res.status_code,200)

        res = self.client.get("/api/author/2f91a911-850f-4655-ac29-9115822c72b5/post/2f91a911-850f-4655-ac29-9115822c72a9/comment/2f91a911-850f-4655-ac29-9115822c72a7/likes")
        body = json.loads(res.content.decode("utf-8"))
        self.assertEqual(len(body["items"]), 2)