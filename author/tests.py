from django.test import TestCase, Client
from author.models import Author
from post.models import Post, Like
from author.views import *
from django.contrib.auth.models import User
from django.utils import timezone
from django.contrib.contenttypes.models import ContentType
# Create your tests here.
class TestAuthorViewsIndex(TestCase):

    def setUp(self):
        Author.objects.create(
            authorID="a6d61bb7-7703-4a6e-a4db-7c8294486a99",
            displayName="author1",
            host="http://ualberta.ca/"
        )
        Author.objects.create(
            authorID="77db03a1-77aa-47e6-8bbc-c61cb158b4ea",
            displayName="author2",
            host="http://ualberta.ca/")
        # values
        self.VIEW_URL = "/service/authors/"

    def testGetAll(self):
        c = Client()
        response = c.get(self.VIEW_URL)
        self.assertEqual(200, response.status_code)
        content = response.json()
        self.assertEqual(2, len(content["items"]))

    def testGetPagination1(self):
        c = Client()
        response = c.get(self.VIEW_URL+"?page=1&size=1")
        self.assertEqual(200, response.status_code)
        content = response.json()
        self.assertEqual(1, len(content["items"]))

    def testGetPagination2(self):
        c = Client()
        response = c.get(self.VIEW_URL+"?page=2&size=2")
        self.assertEqual(200, response.status_code)
        content = response.json()
        self.assertEqual(0, len(content["items"]))

    def testRestrictedHttp(self):
        c = Client()
        responsePOST = c.post(self.VIEW_URL)
        responsePUT = c.put(self.VIEW_URL)
        responseDEL = c.delete(self.VIEW_URL)
        self.assertEqual(405, responsePOST.status_code)
        self.assertEqual(405, responsePUT.status_code)
        self.assertEqual(405, responseDEL.status_code)


class TestAuthorViewsProfile(TestCase):
    def setUp(self) -> None:
        # values
        self.AUTHOR_ID = "a6d61bb7-7703-4a6e-a4db-7c8294486a99"
        self.VIEW_URL = "/service/author/"
        self.DISPLAY_NAME = "testauthor1"
        self.AUTHOR_HOST = "http://ualberta.ca/"
        self.AUTHOR_GIT = "https://github.com/test-username"
        
        Author.objects.create(
            authorID = self.AUTHOR_ID,
            displayName=self.DISPLAY_NAME,
            host= self.AUTHOR_HOST,
            github = self.AUTHOR_GIT
        )

    def testGetUser(self):
        c = Client()
        response = c.get(self.VIEW_URL+self.AUTHOR_ID)
        self.assertEqual(200, response.status_code)
        content = response.json()
        self.assertEqual(self.DISPLAY_NAME, content["displayName"])
        self.assertEqual(self.AUTHOR_HOST, content["host"])
        self.assertEqual(self.AUTHOR_GIT, content["github"])

    def testGetUser404(self):
        c = Client()
        response = c.get(self.VIEW_URL+"c9dce5c5-eb05-44b8-b45d-1f4c6f5b8f09")
        self.assertEqual(404, response.status_code)

    def testPostUpdateUser(self):
        new_id = "29dbad59-7944-4152-9724-4735a749e193"
        new_displayName ="testauthor2"
        new_host = "http://ualberta.ca/"
        new_git = "https://github.com/test"
        new_username = "testuser"
        new_password = "testpassword"

        user = User.objects.create_user(username=new_username, password=new_password)
        Author.objects.create(
            user=user,
            authorID=new_id,
            displayName=new_displayName,
            host=new_host,
            github=new_git
        )

        c = Client()
        c.force_login(user)

        changed_data = {
            "host": new_host,
            "github": new_git,
            "displayName": "changedAuthor"
        }
        response = c.post(
            self.VIEW_URL+new_id,
            changed_data,
            "application/json")
        self.assertEqual(201, response.status_code)
        content = response.json()
        self.assertEqual(changed_data["displayName"], content["displayName"])
        self.assertEqual(new_host, content["host"])
        self.assertEqual(new_git, content["github"])

class TestAuthorViewsInbox(TestCase):
    def setUp(self) -> None:
        # setup two authors to be the inbox sender and recipient
        self.AUTHOR_ID = "a6d61bb7-7703-4a6e-a4db-7c8294486a99"
        self.VIEW_URL = "/service/author/a6d61bb7-7703-4a6e-a4db-7c8294486a99/inbox"
        self.DISPLAY_NAME = "testauthor1"
        self.AUTHOR_HOST = "http://ualberta.ca/"
        self.AUTHOR_GIT = "https://github.com/test-username"
        self.USERNAME = "new_username"
        self.PASSWORD = "new_password"
        self.USER = User.objects.create_user(username=self.USERNAME, password=self.PASSWORD)

        self.AUTHOR_ID2 = "f11920c2-1d32-4ebd-8efb-d21bac08b6a5"
        self.DISPLAY_NAME2 = "testauthor2"
        self.USERNAME2 = "second_username"
        self.PASSWORD2 = "second_password"
        self.USER2 = User.objects.create_user(username=self.USERNAME2, password=self.PASSWORD2)

        self.AUTHOR = Author.objects.create(
            user = self.USER,
            authorID = self.AUTHOR_ID,
            displayName=self.DISPLAY_NAME,
            host= self.AUTHOR_HOST,
            github = self.AUTHOR_GIT
        )
        self.AUTHOR2 = Author.objects.create(
            user = self.USER2,
            authorID = self.AUTHOR_ID2,
            displayName=self.DISPLAY_NAME2,
            host= self.AUTHOR_HOST,
            github = ""
        )

        self.POST_ID = "89af07fa-40c3-4b97-b97d-a0bade92e943"

        # create content for the inbox
        Post.objects.create(
            postID = self.POST_ID,
            ownerID = self.AUTHOR2,
            date = timezone.now(),
            title = "test post",
            content = "text content",
            source = None,
            origin = None,
            description = "test description",
            categories = "wicked;cool",
            isPublic = True,
            isListed = True,
            hasImage = False,
            contentType = "text/markdown"
        )
        Inbox.objects.create(
            authorID = self.AUTHOR,
            inboxType = "post",
            summary = "",
            fromAuthor = self.AUTHOR2,
            date = timezone.now(),
            objectID = self.POST_ID,
            content_type = ContentType.objects.get(model="post")
        )
        Like.objects.create(
            content_type = ContentType.objects.get(model="post"),
            objectID = self.POST_ID,
            authorID = self.AUTHOR2,
            summary = "Post was liked",
            context = None
        )
        Inbox.objects.create(
            authorID = self.AUTHOR,
            inboxType = "like",
            summary = "Liked",
            fromAuthor = self.AUTHOR2,
            date = timezone.now(),
            objectID = self.POST_ID,
            content_type = ContentType.objects.get(model="post")
        )
        Inbox.objects.create(
            authorID = self.AUTHOR,
            inboxType = "follow",
            summary = "someone wants to follow you",
            fromAuthor = self.AUTHOR2,
            date = timezone.now(),
            objectID = None,
            content_type = None
        )

    def testGetInbox(self):
        c = Client()
        c.force_login(self.USER)
        response = c.get(self.VIEW_URL)
        content = response.json()
        self.assertEqual(3, len(content["items"]))
        self.assertEqual(response.status_code, 200)

    def testDeleteInbox(self):
        c = Client()
        c.force_login(self.USER)
        response = c.delete(self.VIEW_URL)
        self.assertEqual(0, Inbox.objects.count())
        self.assertEqual(response.status_code, 200)

    def testSendFollow(self):
        c = Client()
        c.force_login(self.USER)
        post_data = {
            "type": "follow", 
            "summary": "test follow request",
            "actor": {
                "type": "author",
                "id": self.AUTHOR_HOST + "author/" + self.AUTHOR_ID2,
                "url": self.AUTHOR_HOST + "author/" + self.AUTHOR_ID2,
                "host": self.AUTHOR_HOST, "displayName": self.DISPLAY_NAME2,
                "github": ""
            },
            "object": {
                "type": "author",
                "id": self.AUTHOR_HOST + "author/" + self.AUTHOR_ID,
                "host": self.AUTHOR_HOST,
                "displayName": self.DISPLAY_NAME,
                "github": self.AUTHOR_GIT
            }
        }
        response = c.post(
            self.VIEW_URL,
            post_data,
            "application/json")
        self.assertEqual(2, Inbox.objects.filter(inboxType = "follow").count())
        self.assertEqual(response.status_code, 200)

    def testSendLike(self):
        c = Client()
        c.force_login(self.USER)
        Post.objects.create(
            postID = "6a6259fa-8df4-4630-81a9-974f46f9ef66",
            ownerID = self.AUTHOR,
            date = timezone.now(),
            title = "test post",
            content = "text content",
            source = None,
            origin = None,
            description = "test description",
            categories = "wicked;cool",
            isPublic = True,
            isListed = True,
            hasImage = False,
            contentType = "text/markdown"
        )
        post_data = {
            "type": "like", 
            "summary": "test like",
            "@context": self.AUTHOR_HOST,
            "author": {
                "type": "author",
                "id": self.AUTHOR_HOST + "author/" + self.AUTHOR_ID2,
                "url": self.AUTHOR_HOST + "author/" + self.AUTHOR_ID2,
                "host": self.AUTHOR_HOST, "displayName": self.DISPLAY_NAME2,
                "github": ""
            },
            "object": self.AUTHOR_HOST + "author/6a6259fa-8df4-4630-81a9-974f46f9ef66"
        }
        response = c.post(
            self.VIEW_URL,
            post_data,
            "application/json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(2, Inbox.objects.filter(inboxType = "like").count())
        self.assertTrue(Like.objects.filter(objectID="6a6259fa-8df4-4630-81a9-974f46f9ef66").exists())

    def testSendPost(self):
        c = Client()
        c.force_login(self.USER)
        post_data = {
            "type":"post",
            "title":"A post title about a post about web dev",
            "id":"http://127.0.0.1:5454/author/9de17f29c12e8f97bcbbd34cc908f1baba40658e/posts/bd687c13-984e-4a90-8e63-bcb8689b7456",
            "source":"http://lastplaceigotthisfrom.com/posts/yyyyy",
            "origin":"http://whereitcamefrom.com/posts/zzzzz",
            "description":"This post discusses stuff -- brief",
            "contentType":"text/plain",
            "content":"Þā wæs on burgum Bēowulf Scyldinga, lēof lēod-cyning, longe þrāge folcum gefrǣge (fæder ellor hwearf, aldor of earde), oð þæt him eft onwōc hēah Healfdene; hēold þenden lifde, gamol and gūð-rēow, glæde Scyldingas. Þǣm fēower bearn forð-gerīmed in worold wōcun, weoroda rǣswan, Heorogār and Hrōðgār and Hālga til; hȳrde ic, þat Elan cwēn Ongenþēowes wæs Heaðoscilfinges heals-gebedde. Þā wæs Hrōðgāre here-spēd gyfen, wīges weorð-mynd, þæt him his wine-māgas georne hȳrdon, oð þæt sēo geogoð gewēox, mago-driht micel. Him on mōd bearn, þæt heal-reced hātan wolde, medo-ærn micel men gewyrcean, þone yldo bearn ǣfre gefrūnon, and þǣr on innan eall gedǣlan geongum and ealdum, swylc him god sealde, būton folc-scare and feorum gumena. Þā ic wīde gefrægn weorc gebannan manigre mǣgðe geond þisne middan-geard, folc-stede frætwan. Him on fyrste gelomp ǣdre mid yldum, þæt hit wearð eal gearo, heal-ærna mǣst; scōp him Heort naman, sē þe his wordes geweald wīde hæfde. Hē bēot ne ālēh, bēagas dǣlde, sinc æt symle. Sele hlīfade hēah and horn-gēap: heaðo-wylma bād, lāðan līges; ne wæs hit lenge þā gēn þæt se ecg-hete āðum-swerian 85 æfter wæl-nīðe wæcnan scolde. Þā se ellen-gǣst earfoðlīce þrāge geþolode, sē þe in þȳstrum bād, þæt hē dōgora gehwām drēam gehȳrde hlūdne in healle; þǣr wæs hearpan swēg, swutol sang scopes. Sægde sē þe cūðe frum-sceaft fīra feorran reccan",
            "author":{
                    "type":"author",
                "id":"http://127.0.0.1:5454/author/" + self.AUTHOR_ID2,
                "host":"http://127.0.0.1:5454/",
                "displayName":"Lara Croft",
                "url":"http://127.0.0.1:5454/author/" + self.AUTHOR_ID2,
                "github": "http://github.com/laracroft"
            },
            "categories":["web","tutorial"],
            "count": 1023,
            "size": 50,
            "comments":"http://127.0.0.1:5454/author/9de17f29c12e8f97bcbbd34cc908f1baba40658e/posts/de305d54-75b4-431b-adb2-eb6b9e546013/comments",
            "commentsSrc":[
                {
                    "type":"comment",
                    "author":{
                        "type":"author",
                        "id":"http://127.0.0.1:5454/author/" + self.AUTHOR_ID2,
                        "url":"http://127.0.0.1:5454/author/" + self.AUTHOR_ID2,
                        "host":"http://127.0.0.1:5454/",
                        "displayName":"Greg Johnson",
                        "github": "http://github.com/gjohnson"
                    },
                    "comment":"Sick Olde English",
                    "contentType":"text/markdown",
                    "published":"2015-03-09T13:07:04+00:00",
                    "id":"http://127.0.0.1:5454/author/9de17f29c12e8f97bcbbd34cc908f1baba40658e/posts/de305d54-75b4-431b-adb2-eb6b9e546013/comments/f6255bb01c648fe967714d52a89e8e9c",
                }
            ],
            "published":"2015-03-09T13:07:04+00:00",
            "visibility":"PUBLIC",
            "unlisted":False
        }
        response = c.post(
            self.VIEW_URL,
            post_data,
            "application/json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(2, Inbox.objects.filter(inboxType = "post").count())
        print(Post.objects.all())
        self.assertTrue(Post.objects.filter(postID="bd687c13-984e-4a90-8e63-bcb8689b7456").exists())