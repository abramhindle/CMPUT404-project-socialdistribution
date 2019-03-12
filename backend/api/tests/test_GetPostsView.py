from django.contrib.auth.models import User
from django.test import TestCase
from django.test.client import Client, RequestFactory
from rest_framework.test import RequestsClient
from ..models import Post, AuthorProfile, Follow
from ..serializers import PostSerializer
import json
import uuid
from .util import *

class GetPostsTestCase(TestCase):
    client = RequestsClient()
    username1 = "test123"
    password1 = "pw123"
    username2 = "test234"
    password2 = "pw234"

    def setUp(self):
        self.user1 = User.objects.create_user(username=self.username1, password=self.password1)
        self.user2 = User.objects.create_user(username=self.username2, password=self.password2)
        self.user3 = User.objects.create_user(username=self.username3, password=self.password3)
        self.user4 = User.objects.create_user(username=self.username4, password=self.password4)
        self.user5 = User.objects.create_user(username=self.username5, password=self.password5)

        self.authorProfile1 = AuthorProfile.objects.create(
                                                            host="http://127.0.0.1:5454/",
                                                            displayName="Lara Croft",
                                                            github="http://github.com/laracroft",
                                                            user=self.user1)

        self.authorProfile2 = AuthorProfile.objects.create(
                                                            host="http://127.0.0.1:5454/",
                                                            displayName="Lara Croft2",
                                                            github="http://github.com/laracroft2",
                                                            user=self.user2)

        self.authorProfile3 = AuthorProfile.objects.create(host="http://127.0.0.1:5454/",
                                                           displayName="Lara Croft number 3",
                                                           github="http://github.com/laracroft3",
                                                           user=self.user3)

        self.authorProfile4 = AuthorProfile.objects.create(host="http://127.0.0.1:5454/",
                                                           displayName="Lara Croft number 4",
                                                           github="http://github.com/laracroft4",
                                                           user=self.user4)

        self.authorProfile5 = AuthorProfile.objects.create(host="http://127.0.0.1:5454/",
                                                           displayName="Lara Croft number 5",
                                                           github="http://github.com/laracroft5",
                                                           user=self.user5)

        self.public_post1 = {
            "title": "A post title about a post about web dev",
            "source": "http://lastplaceigotthisfrom.com/posts/yyyyy",
            "origin": "http://whereitcamefrom.com/posts/zzzzz",
            "description": "This post discusses stuff -- brief",
            "contentType": "text/plain",
            "content": "public_post content",
            "author": {
                "id": "http://127.0.0.1:5454/author/{}".format(self.authorProfile1.id),
                "host": "http://127.0.0.1:5454/",
                "displayName": self.authorProfile1.displayName,
                "url": "http://127.0.0.1:5454/author/{}".format(self.authorProfile1.id),
                "github": self.authorProfile1.github
            },
            "categories": [],
            "published": "2015-03-09T13:07:04+00:00",
            "id": "de305d54-75b4-431b-adb2-eb6b9e546013",
            "visibility": "PUBLIC",
            "visibleTo": [],
            "unlisted": False
                    }
        self.public_post2 = {
            "title": "A blog about the joys of TDD",
            "source": "http://lastplaceigotthisfrom.com/posts/yyyyy",
            "origin": "http://whereitcamefrom.com/posts/zzzzz",
            "description": "This post discusses stuff -- brief",
            "contentType": "text/plain",
            "content": "public_post content",
            "author": {
                "id": "http://127.0.0.1:5454/author/{}".format(self.authorProfile1.id),
                "host": "http://127.0.0.1:5454/",
                "displayName": self.authorProfile1.displayName,
                "url": "http://127.0.0.1:5454/author/{}".format(self.authorProfile1.id),
                "github": self.authorProfile1.github
            },
            "categories": [],
            "published": "2015-03-09T13:07:04+00:00",
            "id": "de305d54-75b4-431b-adb2-eb6b9e546013",
            "visibility": "PUBLIC",
            "visibleTo": [],
            "unlisted": False
                    }

        self.private_post = {
            "title": "private_post title",
            "source": "http://lastplaceigotthisfrom.com/posts/yyyyy",
            "origin": "http://whereitcamefrom.com/posts/zzzzz",
            "description": "private_post description",
            "contentType": "text/plain",
            "content": "private_post content",
            "author": {
                "id": "http://127.0.0.1:5454/author/{}".format(self.authorProfile1.id),
                "host": "http://127.0.0.1:5454/",
                "displayName": self.authorProfile1.displayName,
                "url": "http://127.0.0.1:5454/author/{}".format(self.authorProfile1.id),
                "github": self.authorProfile1.github
            },
            "categories": [],
            "published": "2015-03-09T13:07:04+00:00",
            "id": "de305d54-75b4-431b-adb2-eb6b9e546013",
            "visibility": "PRIVATE",
            "visibleTo": [],
            "unlisted": False
            }

        self.private_to_author_2 = {
            "title": "private_post title",
            "source": "http://lastplaceigotthisfrom.com/posts/yyyyy",
            "origin": "http://whereitcamefrom.com/posts/zzzzz",
            "description": "private_post description",
            "contentType": "text/plain",
            "content": "private_post content",
            "author": {
                "id": "http://127.0.0.1:5454/author/{}".format(self.authorProfile1.id),
                "host": "http://127.0.0.1:5454/",
                "displayName": self.authorProfile1.displayName,
                "url": "http://127.0.0.1:5454/author/{}".format(self.authorProfile1.id),
                "github": self.authorProfile1.github
            },
            "categories": [],
            "published": "2015-03-09T13:07:04+00:00",
            "id": "de305d54-75b4-431b-adb2-eb6b9e546013",
            "visibility": "PRIVATE",
            "visibleTo": [],
            "unlisted": False
        }
        
        create_mock_post(self.public_post1, self.authorProfile1)
        create_mock_post(self.public_post2, self.authorProfile1)     
        create_mock_post(self.private_post, self.authorProfile1)  

    # def test_get_invalid_auth(self):
    #     response = self.client.get("/api/author/{}/posts".format(self.authorProfile1.id))
    #     self.assertEqual(response.status_code, 403)

    def test_get_public_posts(self):
        self.client.login(username=self.username2, password=self.password2)

        response = self.client.get("/api/author/{}/posts".format(self.authorProfile1.id))
        created_posts = Post.objects.all()

        self.assertEqual(response.status_code, 200)
        assert_post(PostSerializer(created_posts[0]).data, self.public_post1, self.authorProfile1)
        assert_post(PostSerializer(created_posts[1]).data, self.public_post2, self.authorProfile1)

    def test_get_posts_with_invalid_author_id(self):
        self.client.login(username=self.username1, password=self.password1)
        fake_uuid = uuid.uuid4()

        response = self.client.get("/api/author/{}/posts".format(fake_uuid))
        self.assertEqual(response.status_code, 400)
        self.assertEqual(json.loads(response.content), "Error: Author does not exist!")

    def test_get_own_private_post(self):
        # Post.objects.all().delete() #wipe out the db to test privacy settings  
        # create_mock_post(self.private_post, self.authorProfile1)
        self.client.login(username=self.username1, password=self.password1)
        
        response = self.client.get("/api/author/{}/posts".format(self.authorProfile1.id))
        created_posts = Post.objects.all()
        
        self.assertEqual(response.status_code, 200)
        print(len(response.data['posts']))
        #The following assertion asserts that we got a 3rd private post that the author wrote
        assert_post(response.data['posts'][2], self.private_post, self.authorProfile1)

    # this test attempts to see if a user can access another user's private post
    def test_get_private_post(self):
        self.client.login(username=self.username2, password=self.password2)

        response = self.client.get("/api/author/{}/posts".format(self.authorProfile1.id))
        self.assertEqual(response.status_code, 200)

        #This test asserts that author2 can get public posts of author 1 but not the private
        #Currently there are 3 posts in the DB
        self.assertEqual(len(response.data['posts']), 2)

    # This test checks if author 2 can retrieve all posts of author 1 if it is visible to author 2
    def test_get_friends_author_post(self):
        self.client.login()

    def test_get_post_with_id_own_post(self):
        # make sure there's no post existing
        Post.objects.all().delete()
        Follow.objects.all().delete()
        self.client.login(username=self.username5, password=self.password5)

        # public_post_obj = self.create_mock_post(self.public_post, self.authorProfile)
        foaf_post_obj = self.create_mock_post(self.foaf_post, self.authorProfile1)
        # friends_post_obj = self.create_mock_post(self.friends_post, self.authorProfile)
        # private_post_obj = self.create_mock_post(self.private_post, self.authorProfile)
        # server_only_post_obj = self.create_mock_post(self.server_only_post, self.authorProfile)

        Follow.objects.create(authorA=self.user_id,
                            authorB=self.user_id2,
                            status="FRIENDS")

        Follow.objects.create(authorA=self.user_id2,
                            authorB=self.user_id,
                            status="FRIENDS")

        Follow.objects.create(authorA=self.user_id,
                            authorB=self.user_id3,
                            status="FRIENDS")

        Follow.objects.create(authorA=self.user_id3,
                            authorB=self.user_id,
                            status="FRIENDS")

        Follow.objects.create(authorA=self.user_id3,
                            authorB=self.user_id4,
                            status="FRIENDS")

        Follow.objects.create(authorA=self.user_id4,
                            authorB=self.user_id3,
                            status="FRIENDS")

        Follow.objects.create(authorA=self.user_id3,
                            authorB=self.user_id5,
                            status="FRIENDS")

        Follow.objects.create(authorA=self.user_id5,
                            authorB=self.user_id3,
                            status="FRIENDS")

            expected_output = {
                "query": "posts",
                "count": 1,
                "posts": [self.foaf_post]
            }
            expected_author = [self.authorProfile]
            response = self.client.get("/api/posts/{}".format(foaf_post_obj.id))
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.data["query"], expected_output["query"])
            self.assertEqual(response.data["count"], expected_output["count"])

            self.assertEqual(len(response.data["posts"]), 1)
            # for i in range(len(expected_output["posts"])):
                # self.assert_post(response.data["posts"][i], expected_output["posts"][i], expected_author[i])
            self.client.logout()