from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.test import TestCase
from django.contrib.auth.models import User
from .models import NodeModel, AuthorModel, PostsModel
from .serializers import NodeSerializer, AuthorSerializer, FollowModel, AuthorModel


class NodeViewTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin_user = User.objects.create_superuser(username='admin', password='123', email='admin@example.com')
        self.node = NodeModel.objects.create(
            node_url="https://sd7-api.herokuapp.com",
            node_name="Test Node",
            node_user=self.admin_user,
            t16_uname="team16",
            t16_pw="team16pass"
        )
        self.valid_payload = {
            'host': "https://sd7-api.herokuapp.com",
            'resource': "/api/authors/",
            'query': "?page=1&size=25&query="
        }

    def test_authentication(self):
        # Test unauthenticated request
        response = self.client.post(reverse('node-list'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # Test authenticated request
        self.client.login(username='admin', password='123')
        response = self.client.post(reverse('node-list'), data=self.valid_payload)
        self.assertNotEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_permission(self):
        # Test non-admin user
        non_admin = User.objects.create_user(username='nonadmin', password='123')
        self.client.login(username='nonadmin', password='123')
        response = self.client.post(reverse('node-list'), data=self.valid_payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # Test admin user
        self.client.login(username='admin', password='123')
        response = self.client.post(reverse('node-list'), data=self.valid_payload)
        self.assertNotEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_node_view_post(self):
        self.client.login(username='admin', password='123')

        # Test valid payload
        response = self.client.post(reverse('node-list'), data=self.valid_payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Test invalid host
        invalid_payload = self.valid_payload.copy()
        invalid_payload['host'] = "https://invalid-host.example.com"
        response = self.client.post(reverse('node-list'), data=invalid_payload)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        # Test invalid method
        invalid_payload = self.valid_payload.copy()
        invalid_payload['method'] = "DELETE"
        response = self.client.post(reverse('node-list'), data=invalid_payload)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)


class AuthorViewTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='user', password='123', email='user@example.com')
        self.admin_user = User.objects.create_superuser(username='admin', password='123', email='admin@example.com')

        self.author = AuthorModel.objects.create(
            displayName="Test Author",
            github="https://github.com/test_author",
            profileImage="image_data"
        )
        self.author_id = self.author.id

    def test_authentication(self):
        # Test unauthenticated request
        response = self.client.get(reverse('author-detail', kwargs={'author_id': self.author_id}))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # Test authenticated request
        self.client.login(username='user', password='123')
        response = self.client.get(reverse('author-detail', kwargs={'author_id': self.author_id}))
        self.assertNotEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_author_view_get(self):
        self.client.login(username='user', password='123')

        # Test valid author_id
        response = self.client.get(reverse('author-detail', kwargs={'author_id': self.author_id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Test invalid author_id
        response = self.client.get(reverse('author-detail', kwargs={'author_id': 'invalid_author_id'}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_author_view_put(self):
        self.client.login(username='admin', password='123')

        # Test valid payload
        valid_payload = {
            'displayName': 'Updated Author',
            'github': 'https://github.com/updated_author',
            'profileImage': 'updated_image_data'
        }
        response = self.client.put(reverse('author-detail', kwargs={'author_id': self.author_id}), data=valid_payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Test invalid payload
        invalid_payload = {
            'displayName': '',
            'github': 'https://github.com/updated_author',
            'profileImage': 'updated_image_data'
        }
        response = self.client.put(reverse('author-detail', kwargs={'author_id': self.author_id}), data=invalid_payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class TestAuthorModel(TestCase):
    def test_save_author(self):
        author = AuthorModel()
        author.save()

        self.assertIsNotNone(author.pkid)
        self.assertIsNotNone(author.id)
        self.assertIsNotNone(author.host)

class TestAuthorsView(TestCase):
    def setUp(self):
        self.client = APIClient()

    def create_author(self, displayName="John Doe"):
        return AuthorModel.objects.create(displayName=displayName)

    def test_get_authors(self):
        # Create sample authors
        author1 = self.create_author()
        author2 = self.create_author("Jane Doe")

        response = self.client.get(reverse('authors'))

        authors = AuthorModel.objects.all()
        serializer = AuthorSerializer(authors, many=True)
        authors_data = serializer.data[::-1]

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["type"], "authors")
        self.assertEqual(len(response.data["items"]), 2)
        self.assertEqual(response.data["items"], authors_data)

    def test_get_authors_pagination(self):
        # Create sample authors
        for i in range(15):
            self.create_author(f"Author {i+1}")

        response = self.client.get(reverse('authors'), {'page': 2, 'size': 5})

        authors = AuthorModel.objects.all()[5:10]
        serializer = AuthorSerializer(authors, many=True)
        authors_data = serializer.data[::-1]

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["type"], "authors")
        self.assertEqual(len(response.data["items"]), 5)
        self.assertEqual(response.data["items"], authors_data)

    def test_get_authors_search(self):
        # Create sample authors
        self.create_author("John Doe")
        self.create_author("Jane Doe")
        self.create_author("Johnny Appleseed")

        response = self.client.get(reverse('authors'), {'query': 'Doe'})

        authors = AuthorModel.objects.filter(displayName__icontains="Doe")
        serializer = AuthorSerializer(authors, many=True)
        authors_data = serializer.data[::-1]

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["type"], "authors")
        self.assertEqual(len(response.data["items"]), 2)
        self.assertEqual(response.data["items"], authors_data)

    def test_create_author(self):
        new_author_data = {
            "displayName": "New Author",
            "github": "https://github.com/newauthor",
            "profileImage": "data:image/png;base64,encoded_image_data_here",
        }

        response = self.client.post(reverse('authors'), new_author_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class FollowersViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.author1 = AuthorModel.objects.create()
        self.author2 = AuthorModel.objects.create()
        self.author3 = AuthorModel.objects.create()
        self.follow1 = FollowModel.objects.create(follower=self.author1.id, following=self.author2.id, status='friends')
        self.follow2 = FollowModel.objects.create(follower=self.author1.id, following=self.author3.id, status='pending')
        self.follow3 = FollowModel.objects.create(follower=self.author3.id, following=self.author1.id, status='friends')
        self.follow_url = reverse('followers-list', kwargs={'author_id': self.author1.id})

    def test_get_followers(self):
        response = self.client.get(self.follow_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['items']), 1)
        self.assertEqual(response.data['items'][0]['id'], str(self.author3.id))

class FollowViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.author1 = AuthorModel.objects.create()
        self.author2 = AuthorModel.objects.create()
        self.follow1 = FollowModel.objects.create(follower=self.author1.id, following=self.author2.id, status='friends')
        self.follow_url = reverse('follow-detail', kwargs={'author_id': self.author1.id, 'foreign_author_id': self.author2.id})

    def test_get_follow(self):
        response = self.client.get(self.follow_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, 'friends')

    def test_put_follow(self):
        response = self.client.put(self.follow_url, {'status': 'pending'}, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 'pending')

    def test_delete_follow(self):
        response = self.client.delete(self.follow_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

class FollowModelTestCase(TestCase):
    def test_create_follow(self):
        author1 = AuthorModel.objects.create()
        author2 = AuthorModel.objects.create()
        follow = FollowModel.objects.create(follower=author1.id, following=author2.id, status='pending')
        self.assertEqual(follow.status, 'pending')
        self.assertEqual(follow.follower, str(author1.id))
        self.assertEqual(follow.following, str(author2.id))


class PostTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.author = AuthorModel.objects.create(
            username='test_author',
            email='test_author@example.com',
            password='test_author_password'
        )
        self.post_data = {
            'title': 'Test Post',
            'description': 'This is a test post.',
            'contentType': 'text/plain',
            'content': 'Hello, world!',
            'categories': ['test'],
            'visibility': 'PUBLIC',
            'unlisted': False
        }

    def test_create_post(self):
        url = reverse('posts-list', kwargs={'author_id': self.author.id})
        response = self.client.post(url, self.post_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(PostsModel.objects.count(), 1)
        self.assertEqual(PostsModel.objects.get().title, 'Test Post')

    def test_get_all_posts(self):
        post = PostsModel.objects.create(author=self.author, **self.post_data)
        url = reverse('posts-list', kwargs={'author_id': self.author.id})
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['items']), 1)
        self.assertEqual(response.data['items'][0]['title'], post.title)

    def test_get_single_post(self):
        post = PostsModel.objects.create(author=self.author, **self.post_data)
        url = reverse('post-detail', kwargs={'author_id': self.author.id, 'post_id': post.id})
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], post.title)

    def test_update_post(self):
        post = PostsModel.objects.create(author=self.author, **self.post_data)
        url = reverse('post-detail', kwargs={'author_id': self.author.id, 'post_id': post.id})
        updated_data = {
            'title': 'Updated Post',
            'description': 'This is an updated test post.',
            'contentType': 'text/plain',
            'content': 'Hello, world! Updated.',
            'categories': ['test', 'updated'],
            'visibility': 'PUBLIC',
            'unlisted': False
        }
        response = self.client.put(url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        post.refresh_from_db()
        self.assertEqual(post.title, 'Updated Post')

    def test_delete_post(self):
        post = PostsModel.objects.create(author=self.author, **self.post_data)
        url = reverse('post-detail', kwargs={'author_id': self.author.id, 'post_id': post.id})
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(PostsModel.objects.count(), 0)
        
class CommentsViewTest(APITestCase):
    def setUp(self):
        self.client = APIClient()

        # Create test data for Author, Post, and Comment
        self.author = AuthorModel.objects.create(
            id='https://test.com/author/1',
            displayName='test_author'
        )
        self.post = PostsModel.objects.create(
            id='https://test.com/author/1/posts/1',
            title='test_post',
            author=self.author
        )
        self.comment = CommentsModel.objects.create(
            author=self.author,
            comment='test_comment',
            host='https://test.com',
            contentType='text/plain',
            post=self.post
        )

    def test_get_comments(self):
        url = reverse('comments_view', kwargs={'author_id': '1', 'post_id': '1'})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['comments']), 1)
        self.assertEqual(response.data['comments'][0]['comment'], 'test_comment')

    def test_post_comment(self):
        url = reverse('comments_view', kwargs={'author_id': '1', 'post_id': '1'})
        data = {
            'author': AuthorSerializer(self.author).data,
            'comment': 'new_test_comment',
            'host': 'https://test.com',
            'contentType': 'text/plain',
        }
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['comment'], 'new_test_comment')

class LikeViewTest(APITestCase):
    def setUp(self):
        self.client = APIClient()

        # Create test data for Author, Post, and Like
        self.author = AuthorModel.objects.create(
            id='https://test.com/author/1',
            displayName='test_author'
        )
        self.post = PostsModel.objects.create(
            id='https://test.com/author/1/posts/1',
            title='test_post',
            author=self.author
        )
        self.like = LikeModel.objects.create(
            summary='test_like',
            author=self.author,
            object=self.post.id,
            post=self.post
        )

    def test_get_likes(self):
        url = reverse('like_view', kwargs={'author_id': '1', 'post_id': '1'})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['items']), 1)
        self.assertEqual(response.data['items'][0]['summary'], 'test_like')

    def test_post_like(self):
        url = reverse('like_view', kwargs={'author_id': '1', 'post_id': '1'})
        data = {
            'summary': 'new_test_like',
            'author': AuthorSerializer(self.author).data,
            'object': self.post.id,
        }
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['summary'], 'new_test_like')