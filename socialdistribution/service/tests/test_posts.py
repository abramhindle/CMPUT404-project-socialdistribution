from django.test import *
from service.models.author import Author
from service.models.post import Post
from django.contrib.auth.models import User
from service.views.post import *
from django.core.exceptions import ObjectDoesNotExist

from django.urls import reverse

class PostTests(TestCase):
    def setUp(self):
        self.id_view = PostWithId()
        self.creation_view = PostCreation()

        self.user1 = User.objects.create_user("joeguy", "joeguy@email.com", "12345")
        self.user2 = User.objects.create_user("somebody", "somebody@email.com", "1234")

        self.author1 = Author.objects.create(displayName = "Joe Guy", host = "http://localhost:8000", user = self.user1)
        self.author2 = Author.objects.create(displayName = "Somebody Else", host = "http://localhost:8000", user = self.user2)

        self.post1 = Post.objects.create(_id=createPostId(self.author1._id, uuid.uuid4()), title="Hello World!", author=self.author1)
        self.post2 = Post.objects.create(_id=createPostId(self.author2._id, uuid.uuid4()), title="Somebody else's post", author=self.author2)

        print("HERE")
        print(self.post1._id)

        self.request_factory = RequestFactory()

    def tearDown(self):
        self.user1.delete()
        self.user2.delete() 

    def test_get_author_posts(self):

        self.kwargs = {
            'author_id': self.author1._id
        }

        print(self.kwargs["author_id"])

        url = reverse('post_creation', kwargs=self.kwargs) #reverse grabs the full relative url out of urls.py and attaches kwargs
        get_request = self.request_factory.get(url, user = self.user1)
        get_request.user = self.user1

        posts_response = self.creation_view.get(get_request, author_id=self.kwargs["author_id"]) #not sure why i have to pass kwargs in reverse and individually here?

        self.assertEqual(posts_response.status_code, 200)

        paged_posts = json.loads(posts_response.content)

        self.assertTrue("type" in paged_posts)
        self.assertEqual(paged_posts["type"], "posts")
        self.assertTrue("items" in paged_posts)

        posts = paged_posts["items"]
        self.assertTrue(len(posts) == 1) #even though we created a post for author1 and author2, we should only get the post from 1

        self.assertEqual(posts[0]["title"], self.post1.title)
        self.assertEqual(posts[0]["author"]["id"], str(self.author1._id))

    def test_post_author_post(self):
        self.kwargs = {
            'author_id': self.author1._id
        }

        url = reverse('post_creation', kwargs=self.kwargs) #reverse grabs the full relative url out of urls.py and attaches kwargs
        
        body = create_post()

        post_request = self.request_factory.post(url, data=json.dumps(body), content_type = CONTENT_TYPE_JSON)
        post_request.user = self.user1

        posts_response = self.creation_view.post(post_request, author_id=self.kwargs["author_id"])

        self.assertEqual(posts_response.status_code, 201)

        post = Post.objects.get(title=body["title"])

        self.assertEqual(post.author, self.author1)
        self.assertEqual(post.description, body["description"])

    def test_get_post_by_id(self):
        self.kwargs = {
            'author_id': self.author1._id,
            'post_id': self.post1._id
        }

        url = reverse('post_with_id', kwargs=self.kwargs) #reverse grabs the full relative url out of urls.py and attaches kwargs
        
        post_request = self.request_factory.get(url, content_type = CONTENT_TYPE_JSON)
        post_request.user = self.user1

        posts_response = self.id_view.get(post_request, author_id=self.kwargs["author_id"], post_id=self.kwargs["post_id"])

        self.assertEqual(posts_response.status_code, 200)

        posts = json.loads(posts_response.content)

        self.assertEqual(posts["id"], str(self.post1._id))
        self.assertEqual(posts["author"]["id"], str(self.post1.author._id))

    def test_post_post_by_id(self):
        self.kwargs = {
            'author_id': self.author1._id,
            'post_id': self.post1._id
        }

        url = reverse('post_with_id', kwargs=self.kwargs) #reverse grabs the full relative url out of urls.py and attaches kwargs
        
        body = create_post()

        post_request = self.request_factory.post(url, data=json.dumps(body), content_type = CONTENT_TYPE_JSON)
        post_request.user = self.user1

        posts_response = self.id_view.post(post_request, author_id=self.kwargs["author_id"], post_id=self.kwargs["post_id"])
        
        self.assertEqual(posts_response.status_code, 201)

        post = Post.objects.get(_id=self.kwargs["post_id"])

        self.assertEqual(post._id, self.post1._id)
        self.assertEqual(post.title, body["title"])
        self.assertEqual(post.content, body["content"])
        self.assertEqual(post.description, body["description"])
        self.assertEqual(post.contentType, body["contentType"])
        self.assertEqual(post.visibility, body["visibility"])
        self.assertEqual(post.unlisted, body["unlisted"])

    def test_delete_post_by_id(self):
        post_to_delete = Post.objects.create(_id=createPostId(self.author1._id, uuid.uuid4()), author=self.author1) #create a blank object to delete

        self.kwargs = {
            'author_id': self.author1._id,
            'post_id': post_to_delete._id
        }

        post = Post.objects.get(_id=post_to_delete._id)

        if not post:
            self.fail("Object was not created properly, migration may be broken")

        url = reverse('post_with_id', kwargs=self.kwargs) #reverse grabs the full relative url out of urls.py and attaches kwargs


        post_request = self.request_factory.delete(url, content_type = CONTENT_TYPE_JSON)
        post_request.user = self.user1

        posts_response = self.id_view.delete(post_request, author_id=self.kwargs["author_id"], post_id=self.kwargs["post_id"])
        
        self.assertEqual(posts_response.status_code, 202)

        try:
            Post.objects.get(_id=self.kwargs["post_id"])
        except ObjectDoesNotExist:
            pass
        else:
            self.fail("Post should have been deleted")




def create_post():
    return {
        "title": "This is a title!",
        "content":"Lorem Ipsum",
        "description": "I am describing the post",
        "contentType": "text/plain",
        "visibility": "PUBLIC",
        "unlisted": False,
        "categories": [
            "some", "category"
        ]
    }