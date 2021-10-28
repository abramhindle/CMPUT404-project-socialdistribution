from django.test import TestCase, Client
from author.models import Author
from post.models import Post,Like, Comment
from post.views import *
from author.views import *
from django.contrib.auth.models import User
from django.utils import timezone
from django.contrib.contenttypes.models import ContentType
import uuid

class TestPostViewsIndex(TestCase):
    def setUp(self):
        self.author1 = Author.objects.create(
            authorID="a6d61bb7-7703-4a6e-a4db-7c8294486a99",
            displayName="author1",
            host="http://ualberta.ca/"
        )
        Post.objects.create(
            postID = "94580d75-0dd5-43b1-a554-edb28eff0e15",
            ownerID = self.author1,
            date = timezone.now(),
            title = "TEST POST",
            content = "This post is for testing purposes",
            source = "http://lastplaceigotthisfrom.com/posts/yyyyy",
            origin = "http://whereitcamefrom.com/posts/zzzzz",
            description = "This post is for testing purposes",
            isPublic = True,
            isListed = True,
            hasImage = False,
            contentType = "text/plain"
        )

        Post.objects.create(
            postID = uuid.uuid4(),
            ownerID = self.author1,
            date = timezone.now(),
            title = "TEST POST2",
            content = "This post is for testing purposes too",
            source = "http://lastplaceigotthisfrom.com/posts/yyyyy",
            origin = "http://whereitcamefrom.com/posts/zzzzz",
            description = "This post is for testing purposes",
            isPublic = True,
            isListed = True,
            hasImage = False,
            contentType = "text/plain"
        )
        self.VIEW_URL = "/service/author/a6d61bb7-7703-4a6e-a4db-7c8294486a99/posts/"
    def testGetAllUserPosts(self):
        c = Client()
        response = c.get(self.VIEW_URL)
        self.assertEqual(200,response.status_code)
        content = response.json()
        self.assertEqual(2, len(content["items"]))

    def testGetPagination(self):
        c = Client()
        response = c.get(self.VIEW_URL+"?page=1&size=1")
        self.assertEqual(200, response.status_code)
        content = response.json()
        self.assertEqual(1, len(content["items"]))

    
    def testPost(self):
        new_username = "testuser"
        new_password = "testpassword"
        new_authorId = str(uuid.uuid4())
        user = User.objects.create_user(username=new_username, password=new_password)
        authen_user = Author.objects.create(
            user=user,
            authorID=new_authorId,
            displayName="Lara Croft",
            host="http://127.0.0.1:5454/",
            github= "http://github.com/laracroft"
        )

        c = Client()
        c.force_login(user)
        
        new_postID = str(uuid.uuid4())
        #creating a new post
        post_data = {
            "type":"post",
            "title":"A post title about a post about web dev",
            "id":"http://127.0.0.1:5454/author/{}/posts/{}".format(new_authorId,new_postID),
            "source":"http://lastplaceigotthisfrom.com/posts/yyyyy",
            "origin":"http://whereitcamefrom.com/posts/zzzzz",
            "description":"This post discusses stuff -- brief",
            "contentType":"text/plain",
            "content":"Þā wæs on burgum Bēowulf Scyldinga, lēof lēod-cyning, longe þrāge folcum gefrǣge (fæder ellor hwearf, aldor of earde), oð þæt him eft onwōc hēah Healfdene; hēold þenden lifde, gamol and gūð-rēow, glæde Scyldingas. Þǣm fēower bearn forð-gerīmed in worold wōcun, weoroda rǣswan, Heorogār and Hrōðgār and Hālga til; hȳrde ic, þat Elan cwēn Ongenþēowes wæs Heaðoscilfinges heals-gebedde. Þā wæs Hrōðgāre here-spēd gyfen, wīges weorð-mynd, þæt him his wine-māgas georne hȳrdon, oð þæt sēo geogoð gewēox, mago-driht micel. Him on mōd bearn, þæt heal-reced hātan wolde, medo-ærn micel men gewyrcean, þone yldo bearn ǣfre gefrūnon, and þǣr on innan eall gedǣlan geongum and ealdum, swylc him god sealde, būton folc-scare and feorum gumena. Þā ic wīde gefrægn weorc gebannan manigre mǣgðe geond þisne middan-geard, folc-stede frætwan. Him on fyrste gelomp ǣdre mid yldum, þæt hit wearð eal gearo, heal-ærna mǣst; scōp him Heort naman, sē þe his wordes geweald wīde hæfde. Hē bēot ne ālēh, bēagas dǣlde, sinc æt symle. Sele hlīfade hēah and horn-gēap: heaðo-wylma bād, lāðan līges; ne wæs hit lenge þā gēn þæt se ecg-hete āðum-swerian 85 æfter wæl-nīðe wæcnan scolde. Þā se ellen-gǣst earfoðlīce þrāge geþolode, sē þe in þȳstrum bād, þæt hē dōgora gehwām drēam gehȳrde hlūdne in healle; þǣr wæs hearpan swēg, swutol sang scopes. Sægde sē þe cūðe frum-sceaft fīra feorran reccan",
            "author":{
                    "type":"author",
                "id":"http://127.0.0.1:5454/author/" + new_authorId,
                "host":"http://127.0.0.1:5454/",
                "displayName":"Lara Croft",
                "url":"http://127.0.0.1:5454/author/" + new_authorId,
                "github": "http://github.com/laracroft"
            },
            "categories":["web","tutorial"],
            "published":"2015-03-09T13:07:04+00:00",
            "visibility":"PUBLIC",
            "unlisted":False
        }
        
        
        response = c.post(self.VIEW_URL+new_postID,post_data,"application/json")
        self.assertEqual(201, response.status_code)

'''
from django.test import TestCase, Client
from author.models import Author
from author.views import *
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
        Author.objects.create(
            authorID=new_id,
            displayName=new_displayName,
            host=new_host,
            github=new_git
        )

        c = Client()

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
'''