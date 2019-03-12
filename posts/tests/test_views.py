from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIRequestFactory, force_authenticate
from posts.views import UserView, PostView, CommentViewList, PostViewID
from posts.models import User, Post, Comment, Category
from django.forms.models import model_to_dict
from posts.serializers import PostSerializer, UserSerializer
import random
import string



class UserTests(APITestCase):

    def setUp(self):
        self.factory = APIRequestFactory()

    def create_user(self):
        url = reverse('users')
        data = {'displayName': 'test1', 'firstName': 'testFirstName', 'lastName': 'testLastName', 'password1': '1234', 'password2': '1234', 'email': 'test@test.com'}
        request = self.factory.post(url, data=data)
        view = UserView.as_view()
        response = view(request)
        user = User.objects.get(username='test1')
        return user

    def test_user_create_account(self):

        url = reverse('users')
        data = {'displayName': 'test1', 'firstName': 'testFirstName', 'lastName': 'testLastName', 'password1': '1234', 'password2': '1234', 'email': 'test@test.com'}
        request = self.factory.post(url, data=data)
        view = UserView.as_view()
        response = view(request)
        self.assertEqual(response.status_code,status.HTTP_201_CREATED)
        user = User.objects.get(username='test1')
        self.assertFalse(user.approved)

    def test_user_creation_requires_valid_email(self):
        url = reverse('users')
        data = {'displayName': 'test1', 'firstName': 'testFirstName', 'lastName': 'testLastName', 'password1': '1234',
                'password2': '1234', 'email': 'testtest.com'}
        request = self.factory.post(url, data=data)
        view = UserView.as_view()
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_get_info(self):
        user = self.create_user()
        url = reverse('users')
        request = self.factory.get(url)
        view = UserView.as_view()
        force_authenticate(request, user=user)
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['displayName'], user.username)
        self.assertEqual(response.data['lastName'], user.last_name)

    def test_user_update_info(self):
        user = self.create_user()
        url = reverse('users')
        data = {'firstName': 'New First Name'}
        request = self.factory.put(url, data=data)
        view = UserView.as_view()
        force_authenticate(request, user)
        response = view(request)
        self.assertEqual(response.data['firstName'], 'New First Name')


class GeneralFunctions:

    def generate_random_word(self, n):
        word = ''
        for i in range(n):
            word += random.choice(string.ascii_letters)
        return word

    def create_user(self, username="test1", email="test@test.com"):
        data = {'username': username, 'first_name': 'testFirstName',
                'last_name': 'testLastName', 'email': email}
        user = User.objects.create(**data)
        user.set_password("password1")
        user.approved = True
        user.save()
        return user

    def create_post(self, user):
        data = {
            "title": "This is a cool post", "description": "this is a description",
            "content": "This is some content", "author": user
        }
        post = Post.objects.create(**data)
        post.save()
        return post

    def create_comment(self, post, author, comment="default comment"):
        data = {
            "parent_post": post, "author": author, "comment": comment
        }
        comment = Comment.objects.create(**data)
        comment.save()
        return comment


class PostTests(APITestCase):

    def setUp(self):
        self.factory = APIRequestFactory()
        self.helper_functions = GeneralFunctions()

    def test_create_valid_post(self):
        user = self.helper_functions.create_user()
        url = reverse('posts')

        serializer = UserSerializer(instance=user)
        data = {
            'title': 'A post title', 'description': 'A post description',
            'content': 'some content', 'author': serializer.data
        }
        request = self.factory.post(url, data=data, format='json')
        view = PostView.as_view()
        force_authenticate(request, user=user)
        response = view(request)

        # author json object is nested inside post
        author_dict = response.data['author']

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(author_dict['displayName'], user.username)
        self.assertEqual(author_dict['lastName'], user.last_name)

    def test_create_post_with_new_categories(self):
        user = self.helper_functions.create_user()
        url = reverse('posts')

        serializer = UserSerializer(instance=user)

        # this block generates random categories that do not exist yet
        category_input = []
        while len(category_input) < 4:
            word = self.helper_functions.generate_random_word(8)
            try:
                cat_obj = Category.objects.get(category=word)
            except Category.DoesNotExist:
                cat_obj = None

            if cat_obj is None:
                category_input.append(word)

        data = {
            'title': 'A post title', 'description': 'A post description',
            'content': 'some content', 'author': serializer.data, 'categories': category_input
        }
        request = self.factory.post(url, data=data, format='json')
        view = PostView.as_view()
        force_authenticate(request, user=user)
        response = view(request)

        res_categories = response.data['categories']
        self.assertEqual(len(res_categories), 4)
        for cat in category_input:
            self.assertTrue((cat in res_categories))

    def test_create_post_with_existing_categories(self):
        user = self.helper_functions.create_user()
        url = reverse('posts')

        serializer = UserSerializer(instance=user)

        # add categories in database before posting
        category_input = ['web', 'tutorial', 'ajax', 'JAVASCRIPT', 'PyThOn']
        for category in category_input:
            cat_obj = Category.objects.create(category=category)
            cat_obj.save()

        data = {
            'title': 'A post title', 'description': 'A post description',
            'content': 'some content', 'author': serializer.data, 'categories': category_input
        }
        request = self.factory.post(url, data=data, format='json')
        view = PostView.as_view()
        force_authenticate(request, user=user)
        response = view(request)

        res_categories = response.data['categories']
        self.assertEqual(len(res_categories), 5)
        for cat in category_input:
            self.assertTrue((cat in res_categories))

    # tests if user can delete there own post
    def test_delete_self_post(self):
        user = self.helper_functions.create_user()
        post = self.helper_functions.create_post(user)
        url = reverse('postid', args=[post.id])

        request = self.factory.delete(url)
        view = PostViewID.as_view()
        force_authenticate(request, user=user)
        response = view(request, pk=post.id)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    # tests if user can delete someone elses post
    def test_delete_other_post(self):
        user1 = self.helper_functions.create_user(username="darth123", email="darth@vader.com")
        user2 = self.helper_functions.create_user(username="luuuke", email="jedi@master.com")

        post1 = self.helper_functions.create_post(user1)
        url = reverse('postid', args=[post1.id])

        request = self.factory.delete(url)
        view = PostViewID.as_view()
        force_authenticate(request, user=user2)
        response = view(request, pk=post1.id)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_unapproved_user_post(self):
        user = self.helper_functions.create_user()
        user.approved = False
        user.save()
        url = reverse('posts')

        serializer = UserSerializer(instance=user)
        data = {
            'title': 'A post title', 'description': 'A post description',
            'content': 'some content', 'author': serializer.data
        }
        request = self.factory.post(url, data=data, format='json')
        view = PostView.as_view()
        force_authenticate(request, user=user)
        response = view(request)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class CommentTests(APITestCase):

    def setUp(self):
        self.factory = APIRequestFactory()
        self.helper_functions = GeneralFunctions()

    # tests if user can comment on their own post
    def test_create_valid_self_comment(self):
        user = self.helper_functions.create_user()
        post = self.helper_functions.create_post(user)
        url = reverse('comments', args=[post.id])

        serializer = UserSerializer(instance=user)

        data = {'author': serializer.data, 'comment': 'my new comment'}
        request = self.factory.post(url, data=data, format='json')
        view = CommentViewList.as_view()
        force_authenticate(request, user=user)
        response = view(request, post_id=post.id)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['comment'], 'my new comment')
        self.assertEqual(response.data['author']['displayName'], user.username)
        self.assertEqual(response.data['author']['email'], user.email)

    # test if user can comment on someone elses post
    def test_create_valid_other_comment(self):
        user1 = self.helper_functions.create_user()
        user2 = self.helper_functions.create_user(username="test2", email="test2@gmail.com")

        post = self.helper_functions.create_post(user1)
        url = reverse('comments', args=[post.id])

        serializer = UserSerializer(instance=user2)
        # print(serializer.data)

        comment_text = "My name is test2 and I am commenting"
        data = {'author': serializer.data, 'comment': comment_text}
        request = self.factory.post(url, data=data, format='json')
        view = CommentViewList.as_view()
        force_authenticate(request, user=user2)
        response = view(request, post_id=post.id)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['comment'], comment_text)
        self.assertEqual(response.data['author']['displayName'], user2.username)
        self.assertEqual(response.data['author']['email'], user2.email)

    # test if user can delete their own comment
    def test_deleting_self_comment(self):
        # TODO: Implement this once delete is Implemented for comments
        pass

    def test_unapproved_user_comment(self):
        user = self.helper_functions.create_user()
        post = self.helper_functions.create_post(user)
        url = reverse('comments', args=[post.id])
        user.approved = False
        user.save()

        serializer = UserSerializer(instance=user)

        data = {'author': serializer.data, 'comment': 'my new comment'}
        request = self.factory.post(url, data=data, format='json')
        view = CommentViewList.as_view()
        force_authenticate(request, user=user)
        response = view(request, post_id=post.id)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
