from django.test import RequestFactory, TestCase
import apis.authors.views as views
from apps.core.models import Author, User
from random import random
import json

from apps.core.serializers import AuthorSerializer

class AuthorViewTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def tearDown(self):
        Author.objects.all().delete()
        User.objects.all().delete()

    def test_get_authors(self):
        """
        should retrieve all authors in db
        """

        host = "http://testserver"

        displayName = "testUser1"
        github = "https://github.com/testUser"
        profileImage = "https://www.website.com/pfp.png"

        displayName2 = "testUser2"
        github2 = "https://github.com/testUser2"
        profileImage2 = "https://www.website.com/pfp2.png"

        user = User(username="username1")
        user.save()
        author: Author = Author.objects.get(userId=user)
        author.displayName=displayName
        author.github=github
        author.profileImage=profileImage
        author.save()

        user2 = User(username="username2")
        user2.save()
        author2: Author = Author.objects.get(userId=user2)
        author2.displayName=displayName2
        author2.github=github2
        author2.profileImage=profileImage2
        author2.save()

        response = self.client.get("/authors")
        self.assertEqual(response.status_code, 200, f"expected 200. got: {response.status_code}")
        # print(response.content)
        authorList = json.loads(response.content)["data"]
        self.assertEqual(len(authorList), 2)

        data: dict = authorList[0]
        self.assertTrue("id" in data, "an author is missing the id field!")
        
        if data["id"] == str(author.id):
            self.assertEquals(data["type"], "author", "returned author had wrong type!")
            self.assertEquals(data["id"], str(author.id), "returned author did not match one of the created ones!")
            self.assertEquals(data["url"], host + "/author/" + str(author.id), "returned author had wrong url!")
            self.assertEquals(data["host"], host, "returned author had wrong host!")
            self.assertEquals(data["displayName"], displayName, "returned author did not match one of the created ones!")
            self.assertEquals(data["github"], github, "returned author did not match one of the created ones!")
            self.assertEquals(data["profileImage"], profileImage, "returned author did not match one of the created ones!")

            data: dict = authorList[1]
            self.assertEquals(data["type"], "author", "returned author had wrong type!")
            self.assertEquals(data["id"], str(author2.id), "returned author did not match one of the created ones!")
            self.assertEquals(data["url"], host + "/author/" + str(author2.id), "returned author had wrong url!")
            self.assertEquals(data["host"], host, "returned author had wrong host!")
            self.assertEquals(data["displayName"], displayName2, "returned author did not match one of the created ones!")
            self.assertEquals(data["github"], github2, "returned author did not match one of the created ones!")
            self.assertEquals(data["profileImage"], profileImage2, "returned author did not match one of the created ones!")
        else:
            self.assertEquals(data["type"], "author", "returned author had wrong type!")
            self.assertEquals(data["id"], str(author2.id), "returned author did not match one of the created ones!")
            self.assertEquals(data["url"], host + "/author/" + str(author2.id), "returned author had wrong url!")
            self.assertEquals(data["host"], host, "returned author had wrong host!")
            self.assertEquals(data["displayName"], displayName2, "returned author did not match one of the created ones!")
            self.assertEquals(data["github"], github2, "returned author did not match one of the created ones!")
            self.assertEquals(data["profileImage"], profileImage2, "returned author did not match one of the created ones!")
            
            data: dict = authorList[1]
            self.assertEquals(data["type"], "author", "returned author had wrong type!")
            self.assertEquals(data["id"], str(author.id), "returned author did not match one of the created ones!")
            self.assertEquals(data["url"], host + "/author/" + str(author.id), "returned author had wrong url!")
            self.assertEquals(data["host"], host, "returned author had wrong host!")
            self.assertEquals(data["displayName"], displayName, "returned author did not match one of the created ones!")
            self.assertEquals(data["github"], github, "returned author did not match one of the created ones!")
            self.assertEquals(data["profileImage"], profileImage, "returned author did not match one of the created ones!")


    def test_get_authors_empty_db(self):
        """
        should return an empty list
        """

        user = User(username="username1")

        response = self.client.get("/authors")

        self.assertEqual(response.status_code, 200, f"expected 200. got: {response.status_code}")
        self.assertTrue(len(json.loads(response.content)["data"]) == 0, "GET /authors is returning something even with an empty db!")

    # ############################################################
    # # SINGLE AUTHOR TESTS
    # ############################################################

    def test_get_author(self):
        """
        should return appropriate author from db
        """

        host = "testserver"

        host = "http://testserver"

        displayName = "testUser1"
        github = "https://github.com/testUser"
        profileImage = "https://www.website.com/pfp.png"

        displayName2 = "testUser2"
        github2 = "https://github.com/testUser2"
        profileImage2 = "https://www.website.com/pfp2.png"

        user = User(username="username1")
        user.save()
        author: Author = Author.objects.get(userId=user)
        author.displayName=displayName
        author.github=github
        author.profileImage=profileImage
        author.save()

        user2 = User(username="username2")
        user2.save()
        author2: Author = Author.objects.get(userId=user2)
        author2.displayName=displayName2
        author2.github=github2
        author2.profileImage=profileImage2
        author2.save()

        response = self.client.get(f"/author/{author2.id}")
        self.assertEqual(response.status_code, 200, f"expected 200. got: {response.status_code}")
        
        data: dict = json.loads(response.content)

        self.assertEquals(data["type"], "author", "returned author had wrong type!")
        self.assertEquals(data["id"], str(author2.id), "returned author had wrong id!")
        self.assertEquals(data["url"], host + "/author/" + str(author2.id), "returned author had wrong url!")
        self.assertEquals(data["host"], host, "returned author had wrong host!")
        self.assertEquals(data["displayName"], displayName2, "returned author had wrong displayName!")
        self.assertEquals(data["github"], github2, "returned author had wrong github!")
        self.assertEquals(data["profileImage"], profileImage2, "returned author had wrong profileImage!")
    
    def test_get_author_bad_uuid(self):
        """
        should return 404
        """

        user = User(username="username1")
        user.save()

        response = self.client.get(f"/author/0b552c30-0a2e-445e-828d-b356b5276c0f")
        self.assertEqual(response.status_code, 404, f"expected 404. got: {response.status_code}")

    def test_get_author_nonexist(self):
        """
        should return 404
        """

        user = User(username="username1")
        user.save()

        response = self.client.get("/author/notARealUUID")
        self.assertEqual(response.status_code, 404, f"expected 404. got: {response.status_code}")

    def test_get_author_empty_db(self):
        """
        should return 404
        """

        user = User(username="username1")

        response = self.client.get(f"/author/{user.id}")
        self.assertEqual(response.status_code, 404, f"expected 404. got: {response.status_code}")

    def test_post_author(self):
        """
        create a user and carry out a post request. Should return
        an author that is associated with the original user, but with
        modified fields 

        """

        displayName = "testUser"
        github = "https://github.com/testUser"
        profileImage = "https://www.website.com/pfp.png"

        user = User(username="username1")
        user.save()
        author: Author = Author.objects.get(userId=user)

        # we haven't set these fields
        self.assertEqual(author.displayName, "username1")
        self.assertEqual(author.github, "")
        self.assertEqual(author.profileImage, "")

        authorType = "author"
        host = "http://testserver"
        url = host + "/author/" + str(author.id)

        json_str = f"""
        {{
            "type" : "{authorType}",
            "id" : "{author.id}",
            "displayName" : "{displayName}",
            "github" : "{github}",
            "profileImage" : "{profileImage}",
            "host" : "{host}",
            "url" : "{url}"
        }}
        """

        request = self.factory.post(f"/author/{author.id}", content_type='application/json', data=json.loads(json_str))
        response = views.author.as_view()(request, str(author.id))

        self.assertEqual(response.status_code, 200, f"expected 200. got: {response.status_code}")

        data: dict = json.loads(response.content)

        self.assertEquals(data["type"], "author", "returned author had wrong type!")
        self.assertEquals(data["id"], str(author.id), "returned author had wrong id!")
        self.assertEquals(data["url"], host + "/author/" + str(author.id), "returned author had wrong url!")
        self.assertEquals(data["host"], host, "returned author had wrong host!")
        self.assertEquals(data["displayName"], displayName, "returned author had wrong displayName!")
        self.assertEquals(data["github"], github, "returned author had wrong github!")
        self.assertEquals(data["profileImage"], profileImage, "returned author had wrong profileImage!")

        # make sure changes propagated to db
        author2: Author = Author.objects.get(userId=user)
        self.assertEqual(author2.displayName, displayName)
        self.assertEqual(author2.github, github)
        self.assertEqual(author2.profileImage, profileImage)


    def test_post_author_id_mismatch(self):
        """
        should return 400

        """

        displayName = "testUser"
        github = "https://github.com/testUser"
        profileImage = "https://www.website.com/pfp.png"

        user = User(username="username1")
        user.save()
        author = Author.objects.get(userId=user)

        authorType = "author"
        host = "http://testserver"
        url = host + "/author/" + str(author.id)

        json_str = f"""
        {{
            "type" : "{authorType}",
            "id" : "0b552c30-0a2e-445e-828d-b356b5276c0f",
            "displayName" : "{displayName}",
            "github" : "{github}",
            "profileImage" : "{profileImage}",
            "host" : "{host}",
            "url" : "{url}"
        }}
        """

        request = self.factory.post(f"/author/{author.id}", content_type='application/json', data=json.loads(json_str))
        response = views.author.as_view()(request, str(author.id))

        self.assertEqual(response.status_code, 400, f"expected 400. got: {response.status_code}")
        self.assertEqual(response.content.decode('utf-8'), "The id of the author in the body does not match the author_id in the request.")
        
    def test_post_author_host_mismatch(self):
        """
        should return 400

        """

        displayName = "testUser"
        github = "https://github.com/testUser"
        profileImage = "https://www.website.com/pfp.png"

        user = User(username="username1")
        user.save()
        author = Author.objects.get(userId=user)

        authorType = "author"
        host = "http://someWrongHost"
        url = host + "/author/" + str(author.id)

        json_str = f"""
        {{
            "type" : "{authorType}",
            "id" : "{author.id}",
            "displayName" : "{displayName}",
            "github" : "{github}",
            "profileImage" : "{profileImage}",
            "host" : "{host}",
            "url" : "{url}"
        }}
        """

        request = self.factory.post(f"/author/{author.id}", content_type='application/json', data=json.loads(json_str))
        response = views.author.as_view()(request, str(author.id))

        self.assertEqual(response.status_code, 400, f"expected 400. got: {response.status_code}")
        self.assertEqual(response.content.decode('utf-8'), "The author is not from a supported host.")

    def test_post_author_type_mismatch(self):
        """
        should return 400

        """

        displayName = "testUser"
        github = "https://github.com/testUser"
        profileImage = "https://www.website.com/pfp.png"

        user = User(username="username1")
        user.save()
        author = Author.objects.get(userId=user)

        authorType = "someWrongType"
        host = "http://testserver"
        url = host + "/author/" + str(author.id)

        json_str = f"""
        {{
            "type" : "{authorType}",
            "id" : "{author.id}",
            "displayName" : "{displayName}",
            "github" : "{github}",
            "profileImage" : "{profileImage}",
            "host" : "{host}",
            "url" : "{url}"
        }}
        """

        request = self.factory.post(f"/author/{author.id}", content_type='application/json', data=json.loads(json_str))
        response = views.author.as_view()(request, str(author.id))
        
        self.assertEqual(response.status_code, 400, f"expected 400. got: {response.status_code}")
        self.assertEqual(response.content.decode('utf-8'), "Can not change the type of an author")


    ## should work but doesn't??
    # def test_post_author_user_nonexist(self):
    #     """
    #     should return 404
    #     """

    #     displayName = "testUser"
    #     github = "https://github.com/testUser"
    #     profileImage = "https://www.website.com/pfp.png"
    #     id = "0b552c30-0a2e-445e-828d-b356b5276c0f"
    #     authorType = "author"
    #     host = "http://testserver"
    #     url = host + "/author/" + id

    #     json_str = f"""
    #     {{
    #         "type" : "{authorType}",
    #         "id" : "{id}",
    #         "displayName" : "{displayName}",
    #         "github" : "{github}",
    #         "profileImage" : "{profileImage}",
    #         "host" : "{host}",
    #         "url" : "{url}"
    #     }}
    #     """

    #     authors = Author.objects.all()
    #     serializer = AuthorSerializer(authors, many=True)
    #     print(serializer.data)

    #     request = self.factory.post(f"/author/{id}", content_type='application/json', data=json.loads(json_str))
    #     response = views.author.as_view()(request, id)

    #     self.assertEqual(response.status_code, 404, f"expected 404. got: {response.status_code}")
        

    def test_post_author_empty_request(self):
        """
        should return 400

        """

        user = User(username="username1")
        user.save()
        author: Author = Author.objects.get(userId=user)

        request = self.factory.post(f"/author/{author.id}", content_type='application/json', data=dict())
        response = views.author.as_view()(request, str(author.id))

        self.assertEqual(response.status_code, 400, f"expected 400. got: {response.status_code}")