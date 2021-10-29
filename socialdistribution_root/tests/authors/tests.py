from django.test import RequestFactory, TestCase
from apis.authors.dto_models import Author
import apis.authors.views as views
from apps.core.models import User
from random import random
import json

class AuthorModelTests(TestCase):

    def test_contstructor(self):
        """
        Author() returns an Author object with 
        type should be "author", everything else should be None
        """
        author = Author()
        self.assertIs(author.type, "author")
        self.assertIs(author.id, None)
        self.assertIs(author.url, None)
        self.assertIs(author.host, None)
        self.assertIs(author.displayName, None)
        self.assertIs(author.github, None)
        self.assertIs(author.profileImage, None)

    def test_from_user(self):
        """
        author values should be intitialized to that of the user's
        """
        id = "notARealUUID"
        displayName = "testUser"
        github = "https://github.com/testUser"
        profileImage = "https://www.website.com/pfp.png"
        host = "hostname"

        testUser = User(id=id, displayName=displayName, github=github, profileImage=profileImage)
        author = Author.from_user(testUser, host)
        self.assertEqual(author.type, "author")
        self.assertIs(author.id, id, "author did not take on user's id!")
        self.assertIs(author.displayName, displayName, "author did not take on user's displayName!")
        self.assertIs(author.github, github, "author did not take on user's github!")
        self.assertIs(author.profileImage, profileImage, "author did not take on user's profileImage!")
        self.assertIs(author.host, host)
        self.assertEqual(author.url, host + "/service/author/" + id)

    def test_from_user_no_displayName(self):
        """
        author values should be intitialized to that of the user's. 
        displayName should fall back to User's username
        """
        id = "notARealUUID"
        github = "https://github.com/testUser"
        profileImage = "https://www.website.com/pfp.png"
        host = "hostname"

        testUser = User(id=id, github=github, profileImage=profileImage)
        author = Author.from_user(testUser, host)
        self.assertIs(author.id, id)
        self.assertEqual(author.displayName, testUser.username)
        self.assertIs(author.github, github)
        self.assertIs(author.profileImage, profileImage)
        self.assertIs(author.host, host)
        self.assertEqual(author.url, host + "/service/author/" + id)

    def test_from_body(self):
        """
        author should properly have all fields initialized to those in the json string
        (bytearray)
        """
        authorType = "author"
        id = "notARealUUID"
        displayName = "testUser"
        github = "https://github.com/testUser"
        profileImage = "https://www.website.com/pfp.png"
        host = "hostname"
        url = host + "/service/author/" + id

        body  = bytearray(f"""
        {{
            "type" : "{authorType}",
            "id" : "{id}",
            "displayName" : "{displayName}",
            "github" : "{github}",
            "profileImage" : "{profileImage}",
            "host" : "{host}",
            "url" : "{url}"
        }}
        """, 'utf-8')
        
        author = Author.from_body(body)

        self.assertEqual(author.id, id)
        self.assertEqual(author.type, authorType)
        self.assertEqual(author.displayName, displayName)
        self.assertEqual(author.github, github)
        self.assertEqual(author.profileImage, profileImage)
        self.assertEqual(author.host, host)
        self.assertEqual(author.url, url)
        
    def test_from_json(self):
        """
        author should properly have all fields initialized to those in the json string
        """
        authorType = "author"
        id = "notARealUUID"
        displayName = "testUser"
        github = "https://github.com/testUser"
        profileImage = "https://www.website.com/pfp.png"
        host = "hostname"
        url = host + "/service/author/" + id

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

        author = Author.from_json(json_str)

        self.assertEqual(author.type, authorType)
        self.assertEqual(author.id, id)
        self.assertEqual(author.displayName, displayName)
        self.assertEqual(author.github, github)
        self.assertEqual(author.profileImage, profileImage)
        self.assertEqual(author.host, host)
        self.assertEqual(author.url, url)

    def test_from_json_missing_fields(self):
        """
        from_json should should be flexible enough to partially initialize
        """
        authorType = "author"
        id = "notARealUUID"
        displayName = "testUser"
        github = "https://github.com/testUser"
        profileImage = "https://www.website.com/pfp.png"
        host = "hostname"
        url = host + "/service/author/" + id

        potentialContents = {
        0 : f'"type" : "{authorType}",',
        1 : f'"id" : "{id}",',
        2 : f'"displayName" : "{displayName}",',
        3 : f'"github" : "{github}",',
        4 : f'"profileImage" : "{profileImage}",',
        5 : f'"host" : "{host}",',
        6 : f'"url" : "{url}"',
        }

        numFields = 7
        trackers = [0 for n in range(numFields)]

        for i in range(100):
            json_str = "{"
            for j in range(numFields):
                trackers[j] = random()
                if trackers[j] > 0.5:
                    json_str += potentialContents[j]
            json_str = json_str.rstrip(',')
            json_str += "}"
            # print(json_str)
            

            if json_str != "{}":
                # if none of the fields get added, json.loads will throw an error 
                author = Author.from_json(json_str)

                if trackers[0] > 0.5:
                    self.assertEqual(author.type, authorType)
                else: 
                    self.assertEqual(author.type, "author")

                if trackers[1] > 0.5:
                    self.assertEqual(author.id, id)
                else: 
                    self.assertIs(author.id, None)

                if trackers[2] > 0.5:
                    self.assertEqual(author.displayName, displayName)
                else: 
                    self.assertIs(author.displayName, None)
                
                if trackers[3] > 0.5:
                    self.assertEqual(author.github, github)
                else: 
                    self.assertIs(author.github, None)
                
                if trackers[4] > 0.5:
                    self.assertEqual(author.profileImage, profileImage)
                else: 
                    self.assertIs(author.profileImage, None)
                
                if trackers[5] > 0.5:
                    self.assertEqual(author.host, host)
                else: 
                    self.assertIs(author.host, None)
                
                if trackers[6] > 0.5:
                    self.assertEqual(author.url, url)
                else: 
                    self.assertIs(author.url, None)

    def test_to_json(self):
        """
        should produce a json string complete with all of the author's fields
        """
        authorType = "author"
        id = "notARealUUID"
        displayName = "testUser"
        github = "https://github.com/testUser"
        profileImage = "https://www.website.com/pfp.png"
        host = "hostname"
        url = host + "/service/author/" + id

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

        author = Author.from_json(json_str)

        data: dict = json.loads(author.to_json())
        self.assertTrue("type" in data and data["type"] == authorType)
        self.assertTrue("id" in data and data["id"] == id)
        self.assertTrue("displayName" in data and data["displayName"] == displayName)
        self.assertTrue("github" in data and data["github"] == github)
        self.assertTrue("profileImage" in data and data["profileImage"] == profileImage)
        self.assertTrue("host" in data and data["host"] == host)
        self.assertTrue("url" in data and data["url"] == url)

    def test_list_to_json(self):
        """
        should produce a list of dicts that match the list of authors passed in
        """

        numAuthors = 10
        authorList = list()

        for i in range(numAuthors):
            authorType = "author"
            displayName = "testUser"
            github = "https://github.com/testUser"
            profileImage = "https://www.website.com/pfp.png"
            host = "hostname"
            url = host + f"/service/author/{i}"

            json_str = f"""
            {{
                "type" : "{authorType}",
                "id" : "{i}",
                "displayName" : "{displayName}",
                "github" : "{github}",
                "profileImage" : "{profileImage}",
                "host" : "{host}",
                "url" : "{url}"
            }}
            """
            authorList.append(Author.from_json(json_str))

        authorJsonList = json.loads(Author.list_to_json(authorList))

        for i in range(numAuthors):
            data = authorJsonList[i]
            self.assertTrue("type" in data and data["type"] == authorType)
            self.assertTrue("id" in data and data["id"] == f"{i}")
            self.assertTrue("displayName" in data and data["displayName"] == displayName)
            self.assertTrue("github" in data and data["github"] == github)
            self.assertTrue("profileImage" in data and data["profileImage"] == profileImage)
            self.assertTrue("host" in data and data["host"] == host)
            self.assertTrue("url" in data and data["url"] == host + f"/service/author/{i}")

    def test_list_to_json_empty_list(self):
        """
        should return an empty list
        """

        self.assertTrue(len(json.loads(Author.list_to_json(list()))) == 0)

    def test_get_user_id_nonexist(self):
        """
        should return None if author doesn't have an id
        """

        author = Author()
        self.assertIs(author.get_user_id(), None, "an author created through Author() should not have an id!")

    def test_get_user_id_not_in_db(self):
        """
        should return the author's id (in this case an invalid UUID)
        since the actual user hasn't been saved
        """

        id = "notARealUUID"
        displayName = "testUser"
        github = "https://github.com/testUser"
        profileImage = "https://www.website.com/pfp.png"
        host = "hostname"

        testUser = User(id=id, displayName=displayName, github=github, profileImage=profileImage)
        author = Author.from_user(testUser, host)
        self.assertIs(author.get_user_id(), id, "returned user id didn't match author's given id!")

    def test_get_user_id(self):
        """
        should return the correct UUID from database
        """

        id = "0b552c30-0a2e-445e-828d-b356b5276c0f"
        displayName = "testUser"
        github = "https://github.com/testUser"
        profileImage = "https://www.website.com/pfp.png"
        host = "hostname"

        testUser = User(id=id, displayName=displayName, github=github, profileImage=profileImage)
        testUser.save()
        author = Author.from_user(testUser, host)

        self.assertEqual(author.get_user_id(), id, "author id did not match user's!")

    def test_merge_user(self):
        """
        should modify user's displayName, github, and profileImage fields to match author
        """
        
        id = "notARealUUID"
        displayName = "testUser"
        github = "https://github.com/testUser"
        profileImage = "https://www.website.com/pfp.png"
        host = "hostname"

        id2 = "notARealUUID2"
        displayName2 = "testUser2"
        github2 = "https://github.com/testUser2"
        profileImage2 = "https://www.website.com/pfp2.png"
        host2 = "hostname2"

        user = User(id=id, displayName=displayName, github=github, profileImage=profileImage)
        user2 = User(id=id2, displayName=displayName2, github=github2, profileImage=profileImage2)
        
        # users are different
        self.assertNotEqual(user.id, user2.id)
        self.assertNotEqual(user.displayName, user2.displayName)
        self.assertNotEqual(user.github, user2.github)
        self.assertNotEqual(user.profileImage, user2.profileImage)

        author = Author.from_user(user, host)
        mergedUser = author.merge_user(user2)
        
        # author unchanged
        self.assertEqual(author.type, "author", "merging with user shouldn't modify the author!")
        self.assertIs(author.id, id, "merging with user shouldn't modify the author!")
        self.assertIs(author.displayName, displayName, "merging with user shouldn't modify the author!")
        self.assertIs(author.github, github, "merging with user shouldn't modify the author!")
        self.assertIs(author.profileImage, profileImage, "merging with user shouldn't modify the author!")
        self.assertIs(author.host, host, "merging with user shouldn't modify the author!")
        self.assertEqual(author.url, host + "/service/author/" + id), "merging with user shouldn't modify the author!"

        # should be unchaged
        self.assertEqual(mergedUser.id, user2.id, "merging with user shouldn't change the user's id!")
        # should be changed
        self.assertEqual(mergedUser.displayName, user.displayName, "merging with user failed to change the user's displayName!")
        self.assertEqual(mergedUser.github, user.github, "merging with user failed to change the user's github!")
        self.assertEqual(mergedUser.profileImage, user.profileImage, "merging with user failed to change the user's profileImage!")

class AuthorViewTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
    
    # ALL AUTHORS TESTS

    def test_get_authors(self):
        """
        should retrieve all authors in db
        """

        host = "testserver"

        displayName = "testUser"
        github = "https://github.com/testUser"
        profileImage = "https://www.website.com/pfp.png"
        
        displayName2 = "testUser2"
        github2 = "https://github.com/testUser2"
        profileImage2 = "https://www.website.com/pfp2.png"

        user = User(displayName=displayName, github=github, profileImage=profileImage)
        # need to set username for multiple entry into db (apparently username is primary key)
        user.username = str(user.id)
        user.save()
        user2 = User(displayName=displayName2, github=github2, profileImage=profileImage2)
        user2.username = str(user2.id)
        user2.save()

        response = self.client.get("/authors")
        self.assertEqual(response.status_code, 200, f"expected 200. got: {response.status_code}")
        authorList = json.loads(response.content)
        self.assertEqual(len(authorList), 2)

        data: dict = authorList[0]
        self.assertTrue("id" in data, "an author is missing the id field!")

        if data["id"] == str(user.id):
            self.assertEquals(data, json.loads(Author.from_user(user, host).to_json()), "returned author did not match one of the created users")

            data: dict = authorList[1]
            self.assertEquals(data, json.loads(Author.from_user(user2, host).to_json()), "returned author did not match one of the created users")
        else:
            self.assertEquals(data, json.loads(Author.from_user(user2, host).to_json()), "returned author did not match one of the created users")

            data: dict = authorList[1]
            self.assertEquals(data, json.loads(Author.from_user(user, host).to_json()), "returned author did not match one of the created users")

    def test_get_authors_empty_db(self):
        """
        should return an empty list
        """

        displayName = "testUser"
        github = "https://github.com/testUser"
        profileImage = "https://www.website.com/pfp.png"

        user = User(displayName=displayName, github=github, profileImage=profileImage)
        response = self.client.get("/authors")

        self.assertEqual(response.status_code, 200, f"expected 200. got: {response.status_code}")
        self.assertTrue(len(json.loads(response.content)) == 0, "GET /authors is returning something even with an empty db!")

    ############################################################
    # SINGLE AUTHOR TESTS
    ############################################################

    def test_get_author(self):
        """
        should return appropriate author from db
        """

        host = "testserver"

        displayName = "testUser"
        github = "https://github.com/testUser"
        profileImage = "https://www.website.com/pfp.png"

        displayName2 = "testUser2"
        github2 = "https://github.com/testUser2"
        profileImage2 = "https://www.website.com/pfp2.png"

        user = User(displayName=displayName, github=github, profileImage=profileImage)
        # need to set username for multiple entry into db (apparently username is primary key)
        user.username = str(user.id)
        user.save()
        user2 = User(displayName=displayName2, github=github2, profileImage=profileImage2)
        user2.username = str(user2.id)
        user2.save()

        response = self.client.get(f"/author/{user2.id}")
        self.assertEqual(response.status_code, 200, f"expected 200. got: {response.status_code}")
        self.assertEquals(json.loads(response.content), json.loads(Author.from_user(user2, host).to_json()), "data returned from db didn't match user!")
    
    def test_get_author_bad_uuid(self):
        """
        should return 404
        """

        displayName = "testUser"
        github = "https://github.com/testUser"
        profileImage = "https://www.website.com/pfp.png"
        
        user = User(displayName=displayName, github=github, profileImage=profileImage)
        user.save()

        response = self.client.get(f"/author/0b552c30-0a2e-445e-828d-b356b5276c0f")
        self.assertEqual(response.status_code, 404, f"expected 404. got: {response.status_code}")

    def test_get_author_nonexist(self):
        """
        should return 404
        """

        displayName = "testUser"
        github = "https://github.com/testUser"
        profileImage = "https://www.website.com/pfp.png"
        
        user = User(displayName=displayName, github=github, profileImage=profileImage)
        user.save()

        response = self.client.get("/author/notARealUUID")
        self.assertEqual(response.status_code, 404, f"expected 404. got: {response.status_code}")

    def test_get_author_empty_db(self):
        """
        should return 404
        """

        displayName = "testUser"
        github = "https://github.com/testUser"
        profileImage = "https://www.website.com/pfp.png"
        
        user = User(displayName=displayName, github=github, profileImage=profileImage)

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

        user = User(displayName=displayName, github=github, profileImage=profileImage)
        id = user.id
        user.save()

        authorType = "author"
        host = "testserver"
        url = host + "/service/author/" + str(id)

        json_str = f"""
        {{
            "type" : "{authorType}",
            "id" : "{id}",
            "displayName" : "{displayName}2",
            "github" : "{github}2",
            "profileImage" : "{profileImage}2",
            "host" : "{host}",
            "url" : "{url}"
        }}
        """

        request = self.factory.post(f"/author/{id}", content_type='application/json', data=json.loads(json_str))
        # print(json.loads(json_str))
        # print(request.body.decode('utf-8'))
        response = views.author.as_view()(request, id)
        self.assertEqual(response.status_code, 200, f"expected 200. got: {response.status_code}")
        author = Author.from_json(response.content)
        self.assertEqual(author.type, "author")
        self.assertEqual(author.id, str(id), "author id changed!")
        self.assertEqual(author.displayName, f"{displayName}2", "user's displayName was not updated!")
        self.assertEqual(author.github, f"{github}2", "user's github was not updated!")
        self.assertEqual(author.profileImage, f"{profileImage}2", "user's profileImage was not updated!")
        self.assertEqual(author.host, host)
        self.assertEqual(author.url, host + "/service/author/" + str(id))

    def test_post_author_id_mismatch(self):
        """
        should return 400

        """

        displayName = "testUser"
        github = "https://github.com/testUser"
        profileImage = "https://www.website.com/pfp.png"

        user = User(displayName=displayName, github=github, profileImage=profileImage)
        id = user.id
        user.save()

        authorType = "author"
        host = "hostname"
        url = host + "/service/author/" + str(id)

        json_str = f"""
        {{
            "type" : "{authorType}",
            "id" : "0b552c30-0a2e-445e-828d-b356b5276c0f",
            "displayName" : "{displayName}2",
            "github" : "{github}2",
            "profileImage" : "{profileImage}2",
            "host" : "{host}",
            "url" : "{url}"
        }}
        """

        request = self.factory.post(f"/author/{id}", content_type='application/json', data=json.loads(json_str))
        # print(json.loads(json_str))
        # print(request.body.decode('utf-8'))
        response = views.author.as_view()(request, id)
        self.assertEqual(response.status_code, 400, f"expected 400. got: {response.status_code}")
        self.assertEqual(response.content.decode('utf-8'), "The id of the author in the body does not match the author_id in the request.")

    def test_post_author_change_type(self):
        """
        should return 400

        """

        displayName = "testUser"
        github = "https://github.com/testUser"
        profileImage = "https://www.website.com/pfp.png"

        user = User(displayName=displayName, github=github, profileImage=profileImage)
        id = user.id
        user.save()

        authorType = "author"
        host = "hostname"
        url = host + "/service/author/" + str(id)

        json_str = f"""
        {{
            "type" : "someOtherType",
            "id" : "{id}",
            "displayName" : "{displayName}2",
            "github" : "{github}2",
            "profileImage" : "{profileImage}2",
            "host" : "{host}",
            "url" : "{url}"
        }}
        """

        request = self.factory.post(f"/author/{id}", content_type='application/json', data=json.loads(json_str))
        # print(json.loads(json_str))
        # print(request.body.decode('utf-8'))
        response = views.author.as_view()(request, id)
        self.assertEqual(response.status_code, 400, f"expected 400. got: {response.status_code}")

    def test_post_author_user_nonexist(self):
        """
        should return 404
        """

        authorType = "author"
        id = "0b552c30-0a2e-445e-828d-b356b5276c0f"
        displayName = "testUser"
        github = "https://github.com/testUser"
        profileImage = "https://www.website.com/pfp.png"
        host = "hostname"
        url = host + "/service/author/" + id

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

        authorDict = json.loads(json_str)
        request = self.factory.post("/author", content_type='application/json', data=authorDict)
        response = views.author.as_view()(request, "0b552c30-0a2e-445e-828d-b356b5276c0f")
        self.assertEqual(response.status_code, 404, f"expected 404. got: {response.status_code}")

    def test_post_author_empty_request(self):
        """
        should return 400

        """

        displayName = "testUser"
        github = "https://github.com/testUser"
        profileImage = "https://www.website.com/pfp.png"

        user = User(displayName=displayName, github=github, profileImage=profileImage)
        id = user.id
        user.save()

        authorType = "author"
        host = "hostname"
        url = host + "/service/author/" + str(id)

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

        request = self.factory.post(f"/author/{id}", content_type='application/json', data=dict())
        # print(json.loads(json_str))
        # print(request.body.decode('utf-8'))
        response = views.author.as_view()(request, id)
        self.assertEqual(response.status_code, 400, f"expected 400. got: {response.status_code}")