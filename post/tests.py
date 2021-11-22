from django.contrib import auth
from django.test import TestCase, Client
from author.models import Author
from post.models import Post,Like, Comment
from post.views import *
from author.views import *
from django.contrib.auth.models import User
from django.utils import timezone
from django.contrib.contenttypes.models import ContentType
import uuid
import base64
# Create your tests here.
class TestPostViewsComments(TestCase):
    def setUp(self):
        self.AUTHOR_ID = "a10d1b3c-5dae-451b-86bd-900a3f609c15"
        self.USERNAME = "new_username"
        self.PASSWORD = "new_password"
        self.USER = User.objects.create_user(username=self.USERNAME, password=self.PASSWORD)
        self.DISPLAY_NAME = "author1"
        self.HOST = "http://ualberta.ca/"
        self.POST_ID = "3ea43954-7ca4-4107-9e42-1a0f5fa09f15"
        self.AUTHOR = Author.objects.create(
            user = self.USER,
            authorID=self.AUTHOR_ID,
            displayName=self.DISPLAY_NAME,
            host=self.HOST
        )
        self.POST = Post.objects.create(
            postID = self.POST_ID,
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
        self.VIEW_URL = "/service/author/" + self.AUTHOR_ID + "/posts/" + self.POST_ID + "/comments"

    def testGetComments(self):
        Comment.objects.create(
            commentID = "72b207f8-5c7b-4a46-a39d-c9085d218a89",
            postID = self.POST,
            authorID = self.AUTHOR,
            date = timezone.now(),
            content = "Some interesting comment.",
            contentType = "text"
        )
        Comment.objects.create(
            commentID = "af0a5c34-49c9-4314-92f3-88b07f43fab7",
            postID = self.POST,
            authorID = self.AUTHOR,
            date = timezone.now(),
            content = "<h1>Some interesting comment.</h1>",
            contentType = "markdown"
        )

        c = Client()
        c.force_login(self.USER)
        response = c.get(self.VIEW_URL)
        print(response)
        content = response.json()
        self.assertEqual(2, len(content["comments"]))
        self.assertEqual(response.status_code, 200)

    def testPostComment(self):
        post_data = {
            "type": "comment",
            "author": {
                "type": "author",
                "id": self.HOST + "author/" + self.AUTHOR_ID,
                "url": self.HOST + "author/" + self.AUTHOR_ID,
                "host": self.HOST,
                "displayName": self.DISPLAY_NAME,
                "github": None,
                "profileImage": None
            },
            "comment": "A very insightful comment.",
            "contentType": "text/markdown",
            "id": self.HOST + "author/" + self.AUTHOR_ID + "/comments/" + "a111da12-d7ca-4527-858c-80691bb51061",
            "published": "2021-03-09T13:07:04+00:00"
        }
        
        c = Client()
        c.force_login(self.USER)
        response = c.post(self.VIEW_URL, post_data, "application/json")
        self.assertEqual(200, response.status_code)
        self.assertEqual(1, Comment.objects.count())

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
        new_username = "testuser"
        new_password = "testpassword"
        new_authorId = str(uuid.uuid4())
        user = User.objects.create_user(username=new_username, password=new_password)
        Author.objects.create(
            user=user,
            authorID=new_authorId,
            displayName="Lara Croft",
            host="http://127.0.0.1:5454/",
            github= "http://github.com/laracroft"
        )
        c.force_login(user)
        #c.defaults['HTTP_AUTHORIZATION'] = 'Basic ' + self.CREDENTIALS
        response = c.get(self.VIEW_URL)
        self.assertEqual(200,response.status_code)
        content = response.json()
        self.assertEqual(2, len(content["items"]))

    def testGetPagination(self):
        c = Client()
        new_username = "testuser"
        new_password = "testpassword"
        new_authorId = str(uuid.uuid4())
        user = User.objects.create_user(username=new_username, password=new_password)
        Author.objects.create(
            user=user,
            authorID=new_authorId,
            displayName="Lara Croft",
            host="http://127.0.0.1:5454/",
            github= "http://github.com/laracroft"
        )
        c.force_login(user)
        response = c.get(self.VIEW_URL+"?page=1&size=1")
        self.assertEqual(200, response.status_code)
        content = response.json()
        self.assertEqual(1, len(content["items"]))

    def testForbiddenUserPost(self):
        c = Client()
        response = c.post(self.VIEW_URL)
        self.assertEqual(403, response.status_code)
    
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
            "id":None,
            "source":"http://lastplaceigotthisfrom.com/posts/yyyyy",
            "origin":None,
            "description":"This post discusses stuff -- brief",
            "contentType":"text/plain",
            "content":"Þā wæs on burgum Bēowulf Scyldinga, lēof lēod-cyning, longe þrāge folcum gefrǣge (fæder ellor hwearf, aldor of earde), oð þæt him eft onwōc hēah Healfdene; hēold þenden lifde, gamol and gūð-rēow, glæde Scyldingas. Þǣm fēower bearn forð-gerīmed in worold wōcun, weoroda rǣswan, Heorogār and Hrōðgār and Hālga til; hȳrde ic, þat Elan cwēn Ongenþēowes wæs Heaðoscilfinges heals-gebedde. Þā wæs Hrōðgāre here-spēd gyfen, wīges weorð-mynd, þæt him his wine-māgas georne hȳrdon, oð þæt sēo geogoð gewēox, mago-driht micel. Him on mōd bearn, þæt heal-reced hātan wolde, medo-ærn micel men gewyrcean, þone yldo bearn ǣfre gefrūnon, and þǣr on innan eall gedǣlan geongum and ealdum, swylc him god sealde, būton folc-scare and feorum gumena. Þā ic wīde gefrægn weorc gebannan manigre mǣgðe geond þisne middan-geard, folc-stede frætwan. Him on fyrste gelomp ǣdre mid yldum, þæt hit wearð eal gearo, heal-ærna mǣst; scōp him Heort naman, sē þe his wordes geweald wīde hæfde. Hē bēot ne ālēh, bēagas dǣlde, sinc æt symle. Sele hlīfade hēah and horn-gēap: heaðo-wylma bād, lāðan līges; ne wæs hit lenge þā gēn þæt se ecg-hete āðum-swerian 85 æfter wæl-nīðe wæcnan scolde. Þā se ellen-gǣst earfoðlīce þrāge geþolode, sē þe in þȳstrum bād, þæt hē dōgora gehwām drēam gehȳrde hlūdne in healle; þǣr wæs hearpan swēg, swutol sang scopes. Sægde sē þe cūðe frum-sceaft fīra feorran reccan",
            "author":{
                    "type":"author",
                "id":"http://127.0.0.1:8000/author/" + new_authorId,
                "host":"http://127.0.0.1:8000/",
                "displayName":"Lara Croft",
                "url":"http://127.0.0.1:8000/author/" + new_authorId,
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
                        "id":"http://127.0.0.1:5454/author/" + new_authorId,
                        "url":"http://127.0.0.1:5454/author/" + new_authorId,
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
            "unlisted":True
        }
        
        self.VIEW_URL= "/service/author/{}/posts/".format(new_authorId)
        response = c.post(self.VIEW_URL,post_data,"application/json")
        postID_index = response.data["id"].rindex('/')
        new_postID = response.data["id"][postID_index+1:] 
        self.assertEqual(201, response.status_code)
        self.assertTrue(Post.objects.filter(postID=new_postID).exists())
    

class TestPostViews(TestCase):
    def setUp(self):
        new_username = "testuser"
        new_password = "testpassword"
        new_authorId = str(uuid.uuid4())
        self.user = User.objects.create_user(username=new_username, password=new_password)
        self.newAuthorID = uuid.uuid4()
        self.newPostID = uuid.uuid4()
        self.author2 = Author.objects.create(
            user= self.user,
            authorID=self.newAuthorID,
            displayName="author2",
            host="http://ualberta.ca/"
        )
        self.post1 = Post.objects.create(
            postID = self.newPostID,
            ownerID = self.author2,
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
        self.VIEW_URL = "/service/author/{}/posts/".format(self.newAuthorID)
    def testGetPost(self):
        c = Client()
        c.force_login(self.user)
        response = c.get(self.VIEW_URL+str(self.newPostID))
        self.assertEqual(200,response.status_code)
        self.assertEqual(response.data["title"],"TEST POST")
        self.assertEqual(response.data["content"],"This post is for testing purposes")
    
    def testPostUpdatePost(self):
        c = Client()
        c.force_login(self.user)
        new_data = {
            "content":"This post was tested already",
            "description":"Get method for this post worked, what about post?"
        }
        response = c.post(self.VIEW_URL+str(self.newPostID),new_data,"application/json")
        self.assertEqual(201,response.status_code) 
        content = response.json()
        self.assertEqual(new_data["content"],content["content"])
        self.assertEqual(new_data["description"],content["description"])
    
    def testPutCreatePost(self):
        c = Client()
        c.force_login(self.user)
        newPost_ID = str(uuid.uuid4())
        new_post_data = {
            "type": "post",
            "id": "http://127.0.0.1:8000service/author/{}/posts/{}".format(self.newAuthorID,newPost_ID),
            "title": "Hello!",
            "source": "https://www.google.ca/",
            "origin": "https://www.google.ca/",
            "description": "Hope this works.",
            "contentType": "text/plain",
            "content": "Test post <3",
            "author": {
                "type": "author",
                "id": "http://127.0.0.1:8000service/author/{}".format(self.newAuthorID),
                "url": "http://127.0.0.1:8000service/author/{}".format(self.newAuthorID),
                "host": "http://127.0.0.1:8000",
                "displayName": "raoi",
                "github": None,
                "profileImage": None
            },
            "categories": [
                "test,404"
            ],
            "count": 0,
            "comments": "http://127.0.0.1:8000service/author/{}/posts/{}/comments".format(self.newAuthorID,newPost_ID),
            "commentsSrc": [],
            "published": "2021-10-28T20:20:24Z",
            "visibility": "PUBLIC",
            "unlisted": True
        }
        response = c.put(self.VIEW_URL+str(newPost_ID),new_post_data,"application/json")
        self.assertEqual(201,response.status_code) 
        self.assertTrue(Post.objects.filter(postID=newPost_ID).exists())

    def testDeletePost(self):
        c = Client()
        c.force_login(self.user) 
        response = c.delete(self.VIEW_URL+str(self.newPostID))
        self.assertEqual(200,response.status_code)
        self.assertTrue(not Post.objects.filter(postID=self.newPostID).exists())

    def testForbiddenUser(self):
        new_username = "someUser"
        new_password = "somePassword"
        someUser = User.objects.create_user(username=new_username, password=new_password)
        author3 = Author.objects.create(
            user= someUser,
            authorID=uuid.uuid4(),
            displayName="author3",
            host="http://ualberta.ca/"
        ) 
        c = Client() 
        c.force_login(someUser) 
        data = {

        }
        # a user who is not the author of the post is trying to make changes
        responsePost = c.post(self.VIEW_URL+str(self.newPostID),data,"application/json")
        responsePut = c.put(self.VIEW_URL+str(self.newPostID),"application/json")
        responseDelete = c.delete(self.VIEW_URL+str(self.newPostID),data,"application/json") 
        self.assertEqual(403,responsePost.status_code)
        self.assertEqual(403,responsePut.status_code)  
        self.assertEqual(403,responseDelete.status_code) 

class TestLikeViews(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username="new_username", password="new_password")
        self.user2 = User.objects.create_user(username="new_username_some", password="new_password_some")
        self.author_user_1 = uuid.uuid4()
        self.author_user_2 = uuid.uuid4()
        self.author4 = Author.objects.create(
            user= self.user1,
            authorID=self.author_user_1,
            displayName="author1",
            host="http://ualberta.ca/"
        )
        self.author5 = Author.objects.create(
            user= self.user2,
            authorID=self.author_user_2,
            displayName="author2",
            host="http://ualberta.ca/"
        ) 
        post_id = uuid.uuid4()
        
        self.publicPost = Post.objects.create(
            postID = post_id,
            ownerID = self.author4,
            date = timezone.now(),
            title = "TEST POST for liking",
            content = "This post is for testing purposes",
            source = "http://lastplaceigotthisfrom.com/posts/yyyyy",
            origin = "http://whereitcamefrom.com/posts/zzzzz",
            description = "This post is for testing purposes",
            isPublic = True,
            isListed = True,
            hasImage = False,
            contentType = "text/plain"
        )
    
        self.test_like_post = Like.objects.create(
            authorID=self.author5,
            objectID=self.publicPost.postID,
            content_type=ContentType.objects.get(model="post"),
            summary = "This post was liked!"
        )

        self.user3 = User.objects.create_user(username="new_username_some_", password="new_password_some_")
        self.author6 = Author.objects.create(
            user= self.user3,
            authorID=uuid.uuid4(),
            displayName="author2",
            host="http://ualberta.ca/"
        ) 
        
        self.test_comment = Comment.objects.create(
            commentID = uuid.uuid4(),
            postID = self.publicPost,
            authorID = self.author6,
            date = timezone.now(),
            content = "This is a comment!!",
            contentType = "text/plain",

        )

        self.test_like_comment = Like.objects.create(
            authorID=self.author5,
            objectID=self.test_comment.commentID,
            content_type=ContentType.objects.get(model="comment"),
            summary = "This Comment was liked!"
        )
        self.publicPost.save()
        self.test_like_post.save()
        self.test_comment.save()
        self.test_like_comment.save()
        self.VIEW_URL = "/service/author/{}/post/{}/likes".format(self.author_user_1,post_id)

    def testGetLikesPost(self):
        c = Client()
        c.force_login(self.user1)
        c.force_login(self.user2)
        response = c.get(self.VIEW_URL)
        self.assertEqual(200,response.status_code)
        self.assertEqual(1,len(response.data["items"]))

    def testGetLikesComment(self):
        c = Client()
        c.force_login(self.user1)
        c.force_login(self.user2)
        self.VIEW_URL = "/service/author/{}/post/{}/comments/{}/likes".format(self.author_user_1,self.publicPost.postID,self.test_comment.commentID)
        response = c.get(self.VIEW_URL)
        #print(response.data)
        self.assertEqual(200,response.status_code)
