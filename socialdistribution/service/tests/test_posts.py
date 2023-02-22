from django.test import *
from service.models.author import Author
from service.models.posts import Post
from django.contrib.auth.models import User
from service.views.post import *

from django.urls import reverse

class PostTests(TestCase):
    def setUp(self):
        self.post_id = PostWithId()
        self.multiple_view = PostCreation()

        self.user1 = User.objects.create_user("joeguy", "joeguy@email.com", "12345")
        self.user2 = User.objects.create_user("somebody", "somebody@email.com", "1234")

        self.author1 = Author.objects.create(displayName = "Joe Guy", host = "http://localhost:8000", user = self.user1)
        self.author2 = Author.objects.create(displayName = "Somebody Else", host = "http://localhost:8000", user = self.user2)

        self.post1 = Post.objects.create(title="Hello World!", author=self.author1)
        self.post2 = Post.objects.create(title="Somebody else's post", author=self.author2)

        self.request_factory = RequestFactory()

    def tearDown(self):
        self.user1.delete()
        self.user2.delete() 

    def test_get_author_posts(self):

        self.kwargs = {
            'author_id': self.author1._id
        }

        url = reverse('post_creation', kwargs=self.kwargs) #reverse grabs the full relative url out of urls.py and attaches kwargs
        get_request = self.request_factory.get(url, user = self.user1)
        get_request.user = self.user1

        posts_response = self.multiple_view.get(get_request, author_id=self.kwargs["author_id"]) #not sure why i have to pass kwargs in reverse and individually here?

        self.assertEqual(posts_response.status_code, 200)

        paged_posts = json.loads(posts_response.content)

        self.assertTrue("type" in paged_posts)
        self.assertEqual(paged_posts["type"], "posts")
        self.assertTrue("items" in paged_posts)

        posts = paged_posts["items"]
        len(posts)
        self.assertTrue(len(posts) == 1) #even though we created a post for author1 and author2, we should only get the post from 1

        self.assertEqual(posts[0]["title"], self.post1.title)
        self.assertEqual(posts[0]["author"]["id"], str(self.author1._id))

    def test_post_author_post(self):
        self.kwargs = {
            'author_id': self.author1._id
        }

        url = reverse('post_creation', kwargs=self.kwargs) #reverse grabs the full relative url out of urls.py and attaches kwargs
        post_request = self.request_factory.post(url, user = self.user1)
        post_request.user = self.user1

        posts_response = self.multiple_view.post(post_request, author_id=self.kwargs["author_id"])

        self.assertEqual(posts_response.status_code, 201)

