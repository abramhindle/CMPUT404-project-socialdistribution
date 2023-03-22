from django.test import *
from service.models.author import Author
from django.contrib.auth.models import User
from service.models.post import Post
from service.views.inbox import *
from service.views.author import *
from service.views.post import *

from django.urls import reverse

class InboxTests(TestCase):

    def setUp(self):

        self.inbox_view = InboxView()

        self.user1 = User.objects.create_user("joeguy", "joeguy@email.com", "12345")
        self.user2 = User.objects.create_user("somebody", "somebody@email.com", "1234")

        self.author1 = Author.objects.create(displayName = "Joe Guy", host = "http://localhost:8000", user = self.user1) # somebody else creates a post to joe guy's inbox
        self.author2 = Author.objects.create(displayName = "Somebody Else", host = "http://localhost:8000", user = self.user2)

        self.post1 = Post.objects.create(_id=Post.create_post_id(self.author2._id), title="Hello World!", author=self.author2)

        self.comment1 = Comment.objects.create(_id=Comment.create_comment_id(self.author1._id, self.post1._id), comment="This is a comment.", author=self.author1, post=self.post1)

        #self.like1 = Like.objects.create(_id=Like.create_like_id(self.author1._id, self.post1._id), object=self.post1._id, author=self.author1, context="http://localhost", )

        self.request_factory = RequestFactory()
    
    def tearDown(self):
        self.user1.delete()
        self.user2.delete() 
        self.author1.delete()
        self.author2.delete()
        self.post1.delete()
        self.comment1.delete()

    def test_author_inbox_empty_get_200(self):
        self.kwargs = {
            'author_id': self.author1._id
        }

        url = reverse('inbox_view', kwargs=self.kwargs) #reverse grabs the full relative url out of urls.py and attaches kwargs

        get_request = self.request_factory.get(url, user = self.user1)
        get_request.user = self.user1

        inbox_response = self.inbox_view.get(get_request, author_id=self.author1._id)

        self.assertEqual(inbox_response.status_code, 200) #No posts, but author exists, so we should get an empty list

    def test_author_inbox_post_post_202_get_200(self):
        self.kwargs = {
            'author_id': self.author1._id
        }

        post_json = self.post1.toJSON() #push author2's post to author1's inbox

        url = reverse('inbox_view', kwargs=self.kwargs) #reverse grabs the full relative url out of urls.py and attaches kwargs

        post_request = self.request_factory.post(url, user = self.user1, data=json.dumps(post_json), content_type = CONTENT_TYPE_JSON)

        inbox_post_response = self.inbox_view.post(post_request, author_id=self.author1._id)

        self.assertEqual(inbox_post_response.status_code, 202) # was created correctly!

        get_request = self.request_factory.get(url, user = self.user1)

        inbox_response = self.inbox_view.get(get_request, author_id=self.author1._id)

        self.assertEqual(inbox_response.status_code, 200)

        inbox = json.loads(inbox_response.content)

        self.assertEqual(inbox["type"], "inbox")
        self.assertEqual(inbox["author"], self.author1._id)
        self.assertEqual(len(inbox["items"]), 1)

        self.assertEqual(inbox["items"][0]["type"], "post")
        self.assertEqual(inbox["items"][0]["id"], self.post1._id)
        self.assertEqual(inbox["items"][0]["author"]["id"], self.author2._id) #author1 sent to author2 inbox

    def test_author_inbox_post_comment_202_get_200(self):
        self.kwargs = {
            'author_id': self.author2._id
        }

        comment_json = self.comment1.toJSON() #push author2's post to author1's inbox

        url = reverse('inbox_view', kwargs=self.kwargs) #reverse grabs the full relative url out of urls.py and attaches kwargs

        post_request = self.request_factory.post(url, user = self.user2, data=json.dumps(comment_json), content_type = CONTENT_TYPE_JSON)

        inbox_post_response = self.inbox_view.post(post_request, author_id=self.author2._id)

        self.assertEqual(inbox_post_response.status_code, 202) # was created correctly!

        get_request = self.request_factory.get(url, user = self.user2)

        inbox_response = self.inbox_view.get(get_request, author_id=self.author2._id)

        self.assertEqual(inbox_response.status_code, 200)

        inbox = json.loads(inbox_response.content)

        self.assertEqual(inbox["type"], "inbox")
        self.assertEqual(inbox["author"], self.author2._id)
        self.assertEqual(len(inbox["items"]), 1)

        self.assertEqual(inbox["items"][0]["type"], "comment")
        self.assertEqual(inbox["items"][0]["id"], self.comment1._id)
        self.assertEqual(inbox["items"][0]["author"]["id"], self.author1._id) #author1 sent to author2 inbox

    def test_author_inbox_post_comment_202_get_200(self):
        self.kwargs = {
            'author_id': self.author2._id
        }

        comment_json = self.comment1.toJSON() #push author2's post to author1's inbox

        url = reverse('inbox_view', kwargs=self.kwargs) #reverse grabs the full relative url out of urls.py and attaches kwargs

        post_request = self.request_factory.post(url, user = self.user2, data=json.dumps(comment_json), content_type = CONTENT_TYPE_JSON)

        inbox_post_response = self.inbox_view.post(post_request, author_id=self.author2._id)

        self.assertEqual(inbox_post_response.status_code, 202) # was created correctly!

        get_request = self.request_factory.get(url, user = self.user2)

        inbox_response = self.inbox_view.get(get_request, author_id=self.author2._id)

        self.assertEqual(inbox_response.status_code, 200)

        inbox = json.loads(inbox_response.content)

        self.assertEqual(inbox["type"], "inbox")
        self.assertEqual(inbox["author"], self.author2._id)
        self.assertEqual(len(inbox["items"]), 1)

        self.assertEqual(inbox["items"][0]["type"], "comment")
        self.assertEqual(inbox["items"][0]["id"], self.comment1._id)
        self.assertEqual(inbox["items"][0]["author"]["id"], self.author1._id) #author1 sent to author2 inbox


    def test_author_inbox_post_like_202_get_200(self):
        self.kwargs = {
            'author_id': self.author2._id
        }

        url = reverse('inbox_view', kwargs=self.kwargs) #reverse grabs the full relative url out of urls.py and attaches kwargs

        post_request = self.request_factory.post(url, user = self.user2, data=json.dumps(self.create_like(self.author1.toJSON(), self.post1._id)), content_type = CONTENT_TYPE_JSON)

        inbox_post_response = self.inbox_view.post(post_request, author_id=self.author2._id)

        self.assertEqual(inbox_post_response.status_code, 202) # was created correctly!

        get_request = self.request_factory.get(url, user = self.user2)

        inbox_response = self.inbox_view.get(get_request, author_id=self.author2._id)

        self.assertEqual(inbox_response.status_code, 200)

        inbox = json.loads(inbox_response.content)

        self.assertEqual(inbox["type"], "inbox")
        self.assertEqual(inbox["author"], self.author2._id)
        self.assertEqual(len(inbox["items"]), 1)

        self.assertEqual(inbox["items"][0]["type"], "like")
        self.assertEqual(inbox["items"][0]["object"], self.post1._id)
        self.assertEqual(inbox["items"][0]["author"]["id"], self.author1._id)

    def test_author_inbox_comment_like_202_get_200(self): #author 2 likes author 1's comment on their post, so author1 gets an inbox item
        self.kwargs = {
            'author_id': self.author1._id
        }

        url = reverse('inbox_view', kwargs=self.kwargs) #reverse grabs the full relative url out of urls.py and attaches kwargs

        post_request = self.request_factory.post(url, user = self.user1, data=json.dumps(self.create_like(self.author2.toJSON(), self.comment1._id)), content_type = CONTENT_TYPE_JSON)

        inbox_post_response = self.inbox_view.post(post_request, author_id=self.author1._id)

        self.assertEqual(inbox_post_response.status_code, 202) # was created correctly!

        get_request = self.request_factory.get(url, user = self.user1)

        inbox_response = self.inbox_view.get(get_request, author_id=self.author1._id)

        self.assertEqual(inbox_response.status_code, 200)

        inbox = json.loads(inbox_response.content)

        self.assertEqual(inbox["type"], "inbox")
        self.assertEqual(inbox["author"], self.author1._id)
        self.assertEqual(len(inbox["items"]), 1)

        self.assertEqual(inbox["items"][0]["type"], "like")
        self.assertEqual(inbox["items"][0]["object"], self.comment1._id)
        self.assertEqual(inbox["items"][0]["author"]["id"], self.author2._id)

    def test_delete_clear_inbox(self):
        self.kwargs = {
            'author_id': self.author2._id
        }

        comment_json = self.comment1.toJSON() #push author2's post to author1's inbox

        url = reverse('inbox_view', kwargs=self.kwargs) #reverse grabs the full relative url out of urls.py and attaches kwargs

        post_request = self.request_factory.post(url, user = self.user2, data=json.dumps(comment_json), content_type = CONTENT_TYPE_JSON)

        inbox_post_response = self.inbox_view.post(post_request, author_id=self.author2._id)

        self.assertEqual(inbox_post_response.status_code, 202) # was created correctly!

        inbox = Inbox.objects.get(author=self.author2)
        comments = inbox.comments.all()

        self.assertEqual(len(comments), 1)
        #DELETE IT!
        get_request = self.request_factory.delete(url, user = self.user2)

        inbox_response = self.inbox_view.delete(get_request, author_id=self.author2._id)

        self.assertEqual(inbox_response.status_code, 202)
        try:
            inbox = Inbox.objects.get(author=self.author2)
        except ObjectDoesNotExist:
            pass
        else:
            self.fail("Should have been not found")

#TODO: add some tests to make sure only the current user can get their own inbox

    def create_like(self, author, id):
        return {
        "type": "Like",
        "context": "localhost",
        "author": author,
        "object": id
    }