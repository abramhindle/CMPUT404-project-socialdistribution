import json
import uuid
from django.test import TestCase, Client
from rest_framework.test import APIClient

from django.contrib.auth.models import User
from authors.models import Author
from posts.models import Post, Comment, Like

# Create your tests here.
client = APIClient() # the mock http client

class PostTestCase(TestCase):
    def setup_objects(self):
        self.user = User.objects.create_superuser('test_username', 'test_email', 'test_pass')
        client.force_login(self.user)
        self.author = Author.objects.create(user=self.user, display_name=self.user.username)
        self.post = Post.objects.create(
            author = self.author,
            title = "test_title",
            description = "test_description",
            content_type = "PLN",
            content = "test_content",
            visibility = "PUB"
        )
        
    def test_get_post_normal(self):
        self.setup_objects()
        res = client.get(f'/author/{self.author.id}/posts/{self.post.id}/', format='json')
        content = json.loads(res.content)
    
        assert res.status_code == 200
        assert content['type'] == "post"
        assert content['id'] == str(self.post.id)
        assert content['title'] == 'test_title'
        assert content['description'] == 'test_description'
        assert content['contentType'] == 'text/plain'
        assert content['content'] == 'test_content'
        assert content['visibility'] == 'PUBLIC'

    def test_get_post_not_exist(self):
        self.setup_objects()
        res = client.get(f'/author/{self.author.id}/posts/this-id-does-not-exist/', format='json')
        assert res.status_code == 404
    
    def test_get_post_private(self):
        self.setup_objects()
        self.post.visibility = "PRI"
        self.post.save()
        res = client.get(f'/author/{self.author.id}/posts/{self.post.id}/', format='json')
        assert res.status_code == 403

    def test_update_post_normal(self):
        self.setup_objects()
        update_data = {
            'title': 'updated_title',
            'description': 'updated_description',
            'contentType': 'MDN'
        }
        res = client.post(
            f'/author/{self.author.id}/posts/{self.post.id}/', 
            update_data,
            format='json'
        )
        content = json.loads(res.content)
        assert res.status_code == 200
        assert content['title'] == 'updated_title'
        assert content['description'] == 'updated_description'
        assert content['contentType'] == 'text/markdown'

    def test_update_post_not_exist(self):
        self.setup_objects()
        res = client.post(f'/author/{self.author.id}/posts/this-id-does-not-exist/', format='json')
        assert res.status_code == 404
    
    def test_update_post_invalid_entry(self):
        self.setup_objects()
        update_data = {
            # this content type is invalid
            'contentType': 'HTML'
        }
        res = client.post(
            f'/author/{self.author.id}/posts/{self.post.id}/', 
            update_data,
            format='json'
        )
        # should return a bad request
        assert res.status_code == 400

    def test_delete_post_normal(self):
        self.setup_objects()
        res = client.delete(f'/author/{self.author.id}/posts/{self.post.id}/', format='json')
        assert res.status_code == 204
        
        # test whether we can get the post after the DELETE request
        self.assertRaises(Post.DoesNotExist, lambda: Post.objects.get(pk=self.post.id))

    def test_delete_post_not_exist(self):
        self.setup_objects()
        res = client.delete(f'/author/{self.author.id}/posts/this-id-does-not-exist/', format='json')
        assert res.status_code == 404

    def test_put_post_normal(self):
        self.setup_objects()
        new_post_id = str(uuid.uuid4())
        put_data = {
            "title": "new_title",
            "description": "new_description",
            "contentType": "APP",
            "content": "new_content",
            "visibility": "PUB",
            "unlisted": True
        }
        res = client.put(
            f'/author/{self.author.id}/posts/{new_post_id}/',
            put_data,
            format='json'
        )
        assert res.status_code == 204

        new_post = Post.objects.get(pk=new_post_id)
        assert new_post.title == put_data["title"]
        assert new_post.description == put_data["description"]
        assert new_post.content_type == put_data["contentType"]
        assert new_post.content == put_data["content"]
        assert new_post.visibility == put_data["visibility"]
        assert new_post.unlisted == True
    
    def test_put_post_conflict(self):
        self.setup_objects()
        put_data = {
            "title": "new_title",
            "description": "new_description",
            "contentType": "APP",
            "content": "new_content",
            "visibility": "PUB",
            "unlisted": True
        }
        # here I'm trying to create a post with existing post id
        res = client.put(
            f'/author/{self.author.id}/posts/{self.post.id}/',
            put_data,
            format='json'
        )
        assert res.status_code == 409
    
    def test_put_post_invalid_author(self):
        self.setup_objects()
        new_post_id = str(uuid.uuid4())
        random_author_id = str(uuid.uuid4())
        put_data = {
            "title": "new_title",
            "description": "new_description",
            "contentType": "APP",
            "content": "new_content",
            "visibility": "PUB",
            "unlisted": True
        }
        # here I'm trying to create a post 
        # with a random invalid author id
        res = client.put(
            f'/author/{random_author_id}/posts/{new_post_id}/',
            put_data,
            format='json'
        )
        assert res.status_code == 404

    def test_put_post_invalid_entry(self):
        self.setup_objects()
        new_post_id = str(uuid.uuid4())
        # here unlisted as string is invalid
        put_data = {
            "title": "new_title",
            "description": "new_description",
            "contentType": "APP",
            "content": "new_content",
            "visibility": "PUB",
            "unlisted": "True and False"
        }
        res = client.put(
            f'/author/{self.author.id}/posts/{new_post_id}/', 
            put_data,
            format='json'
        )
        # should return a bad request
        assert res.status_code == 400 