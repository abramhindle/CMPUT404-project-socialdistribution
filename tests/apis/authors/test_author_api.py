from django.test import TestCase
from django.urls import reverse
import json

from rest_framework.test import APIClient

from tests.test_helper.auth_helper import AuthHelper

from apps.core.models import Author, User

from uuid import uuid4

class AuthorViewTests(TestCase):
    def createAdmin(self):    
        self.auth_helper = AuthHelper()
        self.auth_helper.setup()
        self.client = APIClient()
        self.auth_helper.authorize_client(self.client)

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

        response = self.client.get(reverse("author:authors"))
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

        response = self.client.get(reverse("author:authors"))

        self.assertEqual(response.status_code, 200, f"expected 200. got: {response.status_code}")
        self.assertEqual(len(json.loads(response.content)["data"]), 0, "GET /authors is returning something even with an empty db!")

    # ############################################################
    # # SINGLE AUTHOR TESTS
    # ############################################################

    # GETs #####################

    def test_get_author(self):
        """
        should return appropriate author from db
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

        response = self.client.get(reverse("author:author", kwargs={"author_id":author2.id}))
        self.assertEqual(response.status_code, 200, f"expected 200. got: {response.status_code}")
        
        data: dict = json.loads(response.content)

        self.assertEquals(data["type"], "author", "returned author had wrong type!")
        self.assertEquals(data["id"], str(author2.id), "returned author had wrong id!")
        self.assertEquals(data["url"], host + "/author/" + str(author2.id), "returned author had wrong url!")
        self.assertEquals(data["host"], host, "returned author had wrong host!")
        self.assertEquals(data["displayName"], displayName2, "returned author had wrong displayName!")
        self.assertEquals(data["github"], github2, "returned author had wrong github!")
        self.assertEquals(data["profileImage"], profileImage2, "returned author had wrong profileImage!")
    
    def test_get_author_nonexist(self):
        """
        should return 404
        """

        user = User(username="username1")
        user.save()
        
        response = self.client.get(reverse("author:author", kwargs={"author_id":uuid4()}))

        self.assertEqual(response.status_code, 404, f"expected 404. got: {response.status_code}")

    def test_get_author_bad_uuid(self):
        """
        should return 404
        """

        user = User(username="username1")
        user.save()

        response = self.client.get(reverse("author:author", kwargs={"author_id":"notARealUUID"}))
        self.assertEqual(response.status_code, 404, f"expected 404. got: {response.status_code}")

    def test_get_author_empty_db(self):
        """
        should return 404
        """

        user = User(username="username1")

        response = self.client.get(reverse("author:author", kwargs={"author_id":user.id}))
        self.assertEqual(response.status_code, 404, f"expected 404. got: {response.status_code}")

    # POSTs ####################

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
        author.save()

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

        self.createAdmin()
        self.auth_helper.get_author()

        response = self.client.post(reverse('author:author', kwargs={'author_id':author.id}), json.loads(json_str), format="json")
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

    def test_post_author_unauthorized(self):
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
        author.save()

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

        response = self.client.post(reverse('author:author', kwargs={'author_id':author.id}), json.loads(json_str), format="json")
        self.assertEqual(response.status_code, 401, f"expected 401. got: {response.status_code}")

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
            "id" : "{uuid4()}",
            "displayName" : "{displayName}",
            "github" : "{github}",
            "profileImage" : "{profileImage}",
            "host" : "{host}",
            "url" : "{url}"
        }}
        """

        self.createAdmin()
        self.auth_helper.get_author()

        response = self.client.post(reverse('author:author', kwargs={'author_id':author.id}), json.loads(json_str), format="json")

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

        self.createAdmin()
        self.auth_helper.get_author()
        
        response = self.client.post(reverse('author:author', kwargs={'author_id':author.id}), json.loads(json_str), format="json")

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

        self.createAdmin()
        self.auth_helper.get_author()
        
        response = self.client.post(reverse('author:author', kwargs={'author_id':author.id}), json.loads(json_str), format="json")
        
        self.assertEqual(response.status_code, 400, f"expected 400. got: {response.status_code}")
        self.assertEqual(response.content.decode('utf-8'), "Can not change the type of an author")

    def test_post_author_user_nonexist(self):
        """
        should return 404
        """

        displayName = "testUser"
        github = "https://github.com/testUser"
        profileImage = "https://www.website.com/pfp.png"
        id = uuid4()
        authorType = "author"
        host = "http://testserver"
        url = host + "/author/" + str(id)

        json_str = f"""
        {{
            "type" : "{authorType}",
            "id" : "{id}",
            "displayName" : "{displayName}",
            "github" : "{github}",
            "profileImage" : "{profileImage}",
            "host" : "{host}",
            "url" : "{url}"
        }}
        """

        self.createAdmin()
        self.auth_helper.get_author()
        
        response = self.client.post(reverse('author:author', kwargs={'author_id':id}), json.loads(json_str), format="json")

        self.assertEqual(response.status_code, 404, f"expected 404. got: {response.status_code}")

    def test_post_author_empty_request(self):
        """
        should return 400

        """

        user = User(username="username1")
        user.save()
        author: Author = Author.objects.get(userId=user)

        self.createAdmin()
        self.auth_helper.get_author()
        
        response = self.client.post(reverse('author:author', kwargs={'author_id':author.id}), {}, format="json")

        self.assertEqual(response.status_code, 400, f"expected 400. got: {response.status_code}")

    # ############################################################
    # # FRIEND AND FOLLOWER TESTS
    # ############################################################

    # PUTs #####################

    def test_put_follower(self):
        """
        should return 200
        """

        user = User(username="username1")
        user.save()
        author: Author = Author.objects.get(userId=user)
        user2 = User(username="username2")
        user2.save()
        author2: Author = Author.objects.get(userId=user2)

        self.createAdmin()
        self.auth_helper.get_author()

        response = self.client.put(reverse('author:follower-info', kwargs={'author_id':author.id, 'foreign_author_id':author2.id}), format="json")
        self.assertEqual(response.status_code, 200, f"expected 200. got: {response.status_code}")

    def test_put_follower_nonexist(self):
        """
        should return 404
        """

        user = User(username="username1")
        user.save()
        author: Author = Author.objects.get(userId=user)

        authorId = uuid4()

        self.createAdmin()
        self.auth_helper.get_author()
        
        response = self.client.put(reverse('author:follower-info', kwargs={'author_id':author.id, 'foreign_author_id':authorId}), format="json")
        self.assertEqual(response.status_code, 404, f"expected 404. got: {response.status_code}")

    def test_put_follower_bad_uuid(self):
        """
        should return 404
        """

        user = User(username="username1")
        user.save()
        author: Author = Author.objects.get(userId=user)

        authorId = "notARealUUID"

        self.createAdmin()
        self.auth_helper.get_author()

        response = self.client.put(reverse('author:follower-info', kwargs={'author_id':author.id, 'foreign_author_id':authorId}), format="json")
        self.assertEqual(response.status_code, 404, f"expected 404. got: {response.status_code}")

    def test_put_follower_author_nonexist(self):
        """
        should return 404
        """

        user = User(username="username1")
        user.save()
        author: Author = Author.objects.get(userId=user)

        authorId = uuid4()

        self.createAdmin()
        self.auth_helper.get_author()

        response = self.client.put(reverse('author:follower-info', kwargs={'author_id':authorId, 'foreign_author_id':author.id}), format="json")
        self.assertEqual(response.status_code, 404, f"expected 404. got: {response.status_code}")

    def test_put_follower_author_bad_uuid(self):
        """
        should return 404
        """

        user = User(username="username1")
        user.save()
        author: Author = Author.objects.get(userId=user)

        authorId = "notARealUUID"

        self.createAdmin()
        self.auth_helper.get_author()

        response = self.client.put(reverse('author:follower-info', kwargs={'author_id':authorId, 'foreign_author_id':author.id}), format="json")
        self.assertEqual(response.status_code, 404, f"expected 404. got: {response.status_code}")

    def test_put_follower_twice(self):
        """
        should return 200
        """

        user = User(username="username1")
        user.save()
        author: Author = Author.objects.get(userId=user)
        user2 = User(username="username2")
        user2.save()
        author2: Author = Author.objects.get(userId=user2)

        self.createAdmin()
        self.auth_helper.get_author()

        response = self.client.put(reverse('author:follower-info', kwargs={'author_id':author.id, 'foreign_author_id':author2.id}), format="json")
        self.assertEqual(response.status_code, 200, f"expected 200. got: {response.status_code}")
        response = self.client.put(reverse('author:follower-info', kwargs={'author_id':author.id, 'foreign_author_id':author2.id}), format="json")
        self.assertEqual(response.status_code, 200, f"expected 200. got: {response.status_code}")

    def test_put_follower_is_one_sided(self):
        user = User(username="username1")
        user.save()
        author: Author = Author.objects.get(userId=user)
        user2 = User(username="username2")
        user2.save()
        author2: Author = Author.objects.get(userId=user2)

        self.createAdmin()
        self.auth_helper.get_author()

        response = self.client.put(reverse('author:follower-info', kwargs={'author_id':author.id, 'foreign_author_id':author2.id}), format="json")
        self.assertEqual(response.status_code, 200, f"expected 200. got: {response.status_code}")

        response = self.client.get(reverse('author:author-followers', kwargs={'author_id':author.id}))
        self.assertEqual(response.status_code, 200, f"expected 200. got: {response.status_code}")
        dict_resp_data = json.loads(response.content)["data"]
        self.assertEqual(len(dict_resp_data), 1, f"expected 1 follow. got: {len(dict_resp_data)}")
        self.assertEqual(dict_resp_data[0]["id"], str(author2.id), "the follow request follows the wrong author!")

        response = self.client.get(reverse('author:author-followers', kwargs={'author_id':author2.id}))
        self.assertEqual(response.status_code, 200, f"expected 200. got: {response.status_code}")
        dict_resp_data = json.loads(response.content)["data"]
        self.assertEqual(len(dict_resp_data), 0, "the request recipient is following the sender!")

    # GETs #####################

    def test_get_followers(self):
        """
        should return a list of the author's appropriate followers
        """
        
        user = User(username="username1")
        user.save()
        author: Author = Author.objects.get(userId=user)
        user2 = User(username="username2")
        user2.save()
        author2: Author = Author.objects.get(userId=user2)
        user3 = User(username="username3")
        user3.save()
        author3: Author = Author.objects.get(userId=user3)

        self.createAdmin()
        self.auth_helper.get_author()

        response = self.client.put(reverse('author:follower-info', kwargs={'author_id':author.id, 'foreign_author_id':author2.id}), format="json")
        self.assertEqual(response.status_code, 200, f"expected 200. got: {response.status_code}")

        response = self.client.put(reverse('author:follower-info', kwargs={'author_id':author2.id, 'foreign_author_id':author.id}), format="json")
        self.assertEqual(response.status_code, 200, f"expected 200. got: {response.status_code}")

        response = self.client.put(reverse('author:follower-info', kwargs={'author_id':author.id, 'foreign_author_id':author3.id}), format="json")
        self.assertEqual(response.status_code, 200, f"expected 200. got: {response.status_code}")

        response = self.client.put(reverse('author:follower-info', kwargs={'author_id':author2.id, 'foreign_author_id':author3.id}), format="json")
        self.assertEqual(response.status_code, 200, f"expected 200. got: {response.status_code}")

        response = self.client.get(reverse('author:author-followers', kwargs={'author_id':author.id}))
        self.assertEqual(response.status_code, 200, f"expected 200. got: {response.status_code}")
        dict_resp_data = json.loads(response.content)["data"]
        self.assertEqual(len(dict_resp_data), 2, f"expected 2 items. got: {len(dict_resp_data)}")

        data1 = dict_resp_data[0]
        data2 = dict_resp_data[1]

        if data1["id"] == str(author3.id):
            temp = data1
            data1 = data2
            data2 = temp

        self.assertEqual(data1["id"], str(author2.id), f"a user got a follow from the wrong author! Expected {str(author2.id)}")
        self.assertEqual(data2["id"], str(author3.id), f"a user got a follow from the wrong author! Expected {str(author3.id)}")

    def test_get_followers_empty(self):
        """
        should return an empty list
        """
        
        user = User(username="username1")
        user.save()
        author: Author = Author.objects.get(userId=user)

        response = self.client.get(reverse('author:author-followers', kwargs={'author_id':author.id}))
        self.assertEqual(response.status_code, 200, f"expected 200. got: {response.status_code}")
        dict_resp_data = json.loads(response.content)["data"]
        self.assertEqual(len(dict_resp_data), 0, "follower list wasn't empty!")

    def test_get_specific_follower(self):
        user = User(username="username1")
        user.save()
        author: Author = Author.objects.get(userId=user)
        user2 = User(username="username2")
        user2.save()
        author2: Author = Author.objects.get(userId=user2)

        self.createAdmin()
        self.auth_helper.get_author()

        response = self.client.put(reverse('author:follower-info', kwargs={'author_id':author.id, 'foreign_author_id':author2.id}), format="json")
        self.assertEqual(response.status_code, 200, f"expected 200. got: {response.status_code}")

        response = self.client.get(reverse('author:follower-info', kwargs={'author_id':author.id, 'foreign_author_id':author2.id}), format="json")
        self.assertEqual(response.status_code, 200, f"expected 200. got: {response.status_code}")
        dict_resp = json.loads(response.content)
        self.assertEqual(dict_resp["id"], str(author2.id), f"incorrect author id! Expected: {str(author2.id)}")

    def test_get_specific_follower_nonexist(self):
        """
        should return 404
        """
        
        user = User(username="username1")
        user.save()
        author: Author = Author.objects.get(userId=user)

        authorId = uuid4()

        response = self.client.get(reverse('author:follower-info', kwargs={'author_id':author.id, 'foreign_author_id':authorId}), format="json")
        self.assertEqual(response.status_code, 404, f"expected 404. got: {response.status_code}")

    def test_get_specific_follower_bad_uuid(self):
        """
        should return 404
        """
        
        user = User(username="username1")
        user.save()
        author: Author = Author.objects.get(userId=user)

        authorId = "notARealUUID"

        response = self.client.get(reverse('author:follower-info', kwargs={'author_id':author.id, 'foreign_author_id':authorId}), format="json")
        self.assertEqual(response.status_code, 404, f"expected 404. got: {response.status_code}")

    def test_get_specific_follower_author_nonexist(self):
        """
        should return 404
        """
        
        user = User(username="username1")
        user.save()
        author: Author = Author.objects.get(userId=user)

        authorId = uuid4()

        response = self.client.get(reverse('author:follower-info', kwargs={'author_id':authorId, 'foreign_author_id':author.id}), format="json")
        self.assertEqual(response.status_code, 404, f"expected 404. got: {response.status_code}")

    def test_get_specific_follower_author_bad_uuid(self):
        """
        should return 404
        """
        
        user = User(username="username1")
        user.save()
        author: Author = Author.objects.get(userId=user)

        authorId = "notARealUUID"

        response = self.client.get(reverse('author:follower-info', kwargs={'author_id':authorId, 'foreign_author_id':author.id}), format="json")
        self.assertEqual(response.status_code, 404, f"expected 404. got: {response.status_code}")

    # DELETEs ################## 

    def test_delete_follower(self):
        """
        should succesfully remove the follower
        """

        user = User(username="username1")
        user.save()
        author: Author = Author.objects.get(userId=user)
        user2 = User(username="username2")
        user2.save()
        author2: Author = Author.objects.get(userId=user2)

        self.createAdmin()
        self.auth_helper.get_author()

        response = self.client.put(reverse('author:follower-info', kwargs={'author_id':author.id, 'foreign_author_id':author2.id}), format="json")
        self.assertEqual(response.status_code, 200, f"expected 200. got: {response.status_code}")

        response = self.client.delete(reverse('author:follower-info', kwargs={'author_id':author.id, 'foreign_author_id':author2.id}), format="json")
        self.assertEqual(response.status_code, 200, f"expected 200. got: {response.status_code}")

        response = self.client.get(reverse('author:author-followers', kwargs={'author_id':author.id}))
        self.assertEqual(response.status_code, 200, f"expected 200. got: {response.status_code}")
        dict_resp_data = json.loads(response.content)["data"]
        self.assertEqual(len(dict_resp_data), 0, "follower list should have been empty but wasn't!")

    def test_delete_follower_nonexist(self):
        """
        should return 404
        """
        
        user = User(username="username1")
        user.save()
        author: Author = Author.objects.get(userId=user)

        authorId = uuid4()

        self.createAdmin()
        self.auth_helper.get_author()

        response = self.client.delete(reverse('author:follower-info', kwargs={'author_id':author.id, 'foreign_author_id':authorId}), format="json")
        self.assertEqual(response.status_code, 404, f"expected 404. got: {response.status_code}")

    def test_delete_follower_bad_uuid(self):
        """
        should return 404
        """
        
        user = User(username="username1")
        user.save()
        author: Author = Author.objects.get(userId=user)

        authorId = "notARealUUID"
        
        self.createAdmin()
        self.auth_helper.get_author()
        
        response = self.client.delete(reverse('author:follower-info', kwargs={'author_id':author.id, 'foreign_author_id':authorId}), format="json")
        self.assertEqual(response.status_code, 404, f"expected 404. got: {response.status_code}")

    def test_delete_follower_author_nonexist(self):
        """
        should return 404
        """
        
        user = User(username="username1")
        user.save()
        author: Author = Author.objects.get(userId=user)

        authorId = uuid4()

        self.createAdmin()
        self.auth_helper.get_author()

        response = self.client.delete(reverse('author:follower-info', kwargs={'author_id':authorId, 'foreign_author_id':author.id}), format="json")
        self.assertEqual(response.status_code, 404, f"expected 200. got: {response.status_code}")

    def test_delete_follower_author_bad_uuid(self):
        """
        should return 404
        """
        
        user = User(username="username1")
        user.save()
        author: Author = Author.objects.get(userId=user)

        authorId = "notARealUUID"

        self.createAdmin()
        self.auth_helper.get_author()

        response = self.client.delete(reverse('author:follower-info', kwargs={'author_id':authorId, 'foreign_author_id':author.id}), format="json")
        self.assertEqual(response.status_code, 404, f"expected 404. got: {response.status_code}")

    def test_delete_non_follower(self):
        """
        sould return 404
        """

        user = User(username="username1")
        user.save()
        author: Author = Author.objects.get(userId=user)
        user2 = User(username="username2")
        user2.save()
        author2: Author = Author.objects.get(userId=user2)

        self.createAdmin()
        self.auth_helper.get_author()

        response = self.client.delete(reverse('author:follower-info', kwargs={'author_id':author.id, 'foreign_author_id':author2.id}), format="json")
        self.assertEqual(response.status_code, 404, f"expected 404. got: {response.status_code}")

    def test_delete_follower_twice(self):
        """
        should succesfully remove the follower, then return 404
        """

        user = User(username="username1")
        user.save()
        author: Author = Author.objects.get(userId=user)
        user2 = User(username="username2")
        user2.save()
        author2: Author = Author.objects.get(userId=user2)

        self.createAdmin()
        self.auth_helper.get_author()

        response = self.client.put(reverse('author:follower-info', kwargs={'author_id':author.id, 'foreign_author_id':author2.id}), format="json")
        self.assertEqual(response.status_code, 200, f"expected 200. got: {response.status_code}")

        response = self.client.delete(reverse('author:follower-info', kwargs={'author_id':author.id, 'foreign_author_id':author2.id}), format="json")
        self.assertEqual(response.status_code, 200, f"expected 200. got: {response.status_code}")

        response = self.client.get(reverse('author:author-followers', kwargs={'author_id':author.id}))
        self.assertEqual(response.status_code, 200, f"expected 200. got: {response.status_code}")
        dict_resp_data = json.loads(response.content)["data"]
        self.assertEqual(len(dict_resp_data), 0, "follower list should have been empty but wasn't!")

        response = self.client.delete(reverse('author:follower-info', kwargs={'author_id':author.id, 'foreign_author_id':author2.id}), format="json")
        self.assertEqual(response.status_code, 404, f"expected 404. got: {response.status_code}")