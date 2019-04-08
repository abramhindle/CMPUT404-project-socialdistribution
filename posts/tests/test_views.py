from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIRequestFactory, force_authenticate
from posts.viewsfolder.author_following_views import FriendListView, AreFriendsView, FollowReqListView, \
    FriendRequestView, FollowView
from posts.views import UserView
from posts.viewsfolder.comment_views import CommentViewList
from posts.viewsfolder.post_views import PostView, PostViewID
from posts.models import User, Post, Comment, Category, Follow, FollowRequest, Viewer, WWUser
from posts.helpers import get_local_user_url, parse_id_from_url, get_ww_user
from preferences import preferences
from posts.serializers import UserSerializer, FollowSerializer
import random
import string


class GeneralFunctions:

    def generate_random_word(self, n):
        word = ''
        for i in range(n):
            word += random.choice(string.ascii_letters)
        return word

    def get_user_by_username(self, username):
        try:
            return User.objects.get(username=username)
        except:
            return None

    def create_user(self, username="test1", email="test@test.com"):
        data = {'username': username, 'first_name': 'testFirstName', 'displayName': username,
                'last_name': 'testLastName', 'email': email, 'password1': "password1", 'password2': 'password1'}
        user = UserSerializer(data=data, context={'create': True})
        user.is_valid()
        user.save()
        user_model = User.objects.get(pk=parse_id_from_url(user.data['id']))
        user_model.approved = True
        user_model.save()
        return user_model

    def create_post(self, user):
        data = {
            "title": "This is a cool post", "description": "this is a description",
            "content": "This is some content", "author": user
        }
        post = Post.objects.create(**data)
        post.save()
        return post

    def create_comment(post, author, comment="default comment"):
        data = {
            "parent_post": post, "author": author, "comment": comment
        }
        comment = Comment.objects.create(**data)
        comment.save()
        return comment

    def create_follow(self, user, followee):
        ww_user = WWUser.objects.get(user_id=user.id)
        ww_followee = WWUser.objects.get(user_id=followee.id)
        follow = Follow(followee=ww_followee, follower=ww_user)
        follow.save()
        return follow

    def create_foaf(self, user1, user2, user3):
        self.create_follow(user1, user3)
        self.create_follow(user3, user1)
        self.create_follow(user2, user3)
        self.create_follow(user3, user2)

    def create_followrequest(self, user, other):
        ww_user = get_ww_user(user.id)
        ww_other = get_ww_user(other.id)
        followreq = FollowRequest(requester=ww_user, requestee=ww_other)
        followreq.save()
        return followreq


class UserTests(APITestCase):

    def setUp(self):
        self.factory = APIRequestFactory()
        self.helper_functions = GeneralFunctions()

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


class PostTests(APITestCase):

    def setUp(self):
        self.factory = APIRequestFactory()
        self.helper_functions = GeneralFunctions()

    def test_create_valid_post(self):
        user = self.helper_functions.create_user()
        url = reverse('posts')

        # serializer = UserSerializer(instance=user, context={'request':request})
        # TODO: remove serializer.data
        data = {
            'title': 'A post title', 'description': 'A post description',
            'content': 'some content'
        }
        request = self.factory.post(url, data=data, format='json')
        # serializer = UserSerializer(instance=user, context={'request':request})
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

        # TODO: remove serializer.data
        data = {
            'title': 'A post title', 'description': 'A post description',
            'content': 'some content', 'categories': category_input
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

        # TODO: remove serializer.data
        data = {
            'title': 'A post title', 'description': 'A post description',
            'content': 'some content', 'categories': category_input
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

    def test_post_foaf(self):
        user1 = self.helper_functions.create_user(username="alan")
        user2 = self.helper_functions.create_user(username="ada")
        user3 = self.helper_functions.create_user(username="church")
        self.helper_functions.create_foaf(user1, user2, user3)

        postdata = {
            "title": "This is a cool post", "description": "this is a description",
            "content": "This is some content", "author": user1, "visibility": "FOAF"
        }
        post = Post.objects.create(**postdata)
        post.save()
        userserializer = UserSerializer(instance=user2)
        url = reverse('postid', args=[post.id])
        data = {
            "query": "getPost",
            "postid": post.id,
            "url": url,
            "author": userserializer.data,
            # friends of author
            "friends": [str(user3.id)]
        }
        request = self.factory.post(url, data=data, format='json')
        view = PostViewID.as_view()
        force_authenticate(request, user=user2)
        response = view(request, pk=post.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

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

    def test_not_serving_images(self):
        user = self.helper_functions.create_user(username="alan")

        postdata = {
            "title": "This is a cool post", "description": "this is a description",
            "content": "This is some content", "author": user, "visibility": "FOAF",
            "contentType": "img/png;base64"
        }
        post = Post.objects.create(**postdata)
        post.save()

        prefs = preferences.SitePreferences
        prefs.serve_others_images = False
        prefs.save()

        url = reverse('postid', args={post.id})
        request = self.factory.get(url)
        view = PostViewID.as_view()
        force_authenticate(request, user=user)
        response = view(request, pk=post.id)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_filter_images(self):
        user = self.helper_functions.create_user('mikeyp')
        self.helper_functions.create_post(user)
        image_post = self.helper_functions.create_post(user)
        image_post.contentType = "img/png;base64"
        # objects created through the serializer do this so we should for this test too
        image_post.unlisted = True
        image_post.save()

        prefs = preferences.SitePreferences
        prefs.serve_others_images = False
        prefs.save()

        url = reverse('posts')
        request = self.factory.get(url)
        view = PostView.as_view()
        force_authenticate(request, user)
        response = view(request)
        self.assertEqual(len(response.data["posts"]), 1)

    def test_post_pagination(self):
        user = self.helper_functions.create_user("tlazASAP")
        self.helper_functions.create_post(user)
        self.helper_functions.create_post(user)

        url = reverse('posts')
        request = self.factory.get(url)
        view = PostView.as_view()
        force_authenticate(request, user)
        response = view(request)
        self.assertEqual(response.data["query"], "posts")
        self.assertEqual(response.data["count"], 2)

    def test_post_pagination_with_size_paramater(self):
        user = self.helper_functions.create_user("tlazASAP")
        self.helper_functions.create_post(user)
        self.helper_functions.create_post(user)

        url = reverse('posts')
        request = self.factory.get(url + "?size=1")
        view = PostView.as_view()
        force_authenticate(request, user)
        response = view(request)
        self.assertEqual(response.data["query"], "posts")
        self.assertEqual(response.data["size"], 1)
        self.assertEqual(response.data["next"], request.build_absolute_uri("/posts/") + "?page=2&size=1")

    def test_create_valid_private_post_with_visible_to_field(self):
        user = self.helper_functions.create_user()
        url = reverse('posts')
        u1_url = 'http://127.0.0.1:5454/author/1d698d25ff008f7538453c120f581471'
        u2_url = 'http://127.0.0.1:5454/author/9de17f29c12e8f97bcbbd34cc908f1baba40658e'

        data = {
            'title': 'A post title', 'description': 'A post description',
            'content': 'some content', 'visibleTo': [u1_url, u2_url], 'visibility': 'PRIVATE'
        }
        request = self.factory.post(url, data=data, format='json')
        view = PostView.as_view()
        force_authenticate(request, user=user)
        response = view(request)

        res_visible_to = response.data['visibleTo']
        self.assertEqual(len(res_visible_to), 2)
        self.assertIn(u1_url, res_visible_to)
        self.assertIn(u2_url, res_visible_to)

    def test_get_post_with_visible_to_field(self):
        user = self.helper_functions.create_user()
        post = self.helper_functions.create_post(user)
        u1_url = 'http://127.0.0.1:5454/author/1d698d25ff008f7538453c120f581471'
        viewer1 = Viewer.objects.create(url=u1_url, post=post)
        u2_url = 'http://127.0.0.1:5454/author/9de17f29c12e8f97bcbbd34cc908f1baba40658e'
        viewer2 = Viewer.objects.create(url=u2_url, post=post)

        url = reverse('postid', args=[post.id])
        request = self.factory.get(url)
        view = PostViewID.as_view()
        force_authenticate(request, user=user)
        response = view(request, pk=post.id)

        res_visible_to = response.data[0]['visibleTo']
        self.assertEqual(len(res_visible_to), 2)
        self.assertIn(u1_url, res_visible_to)
        self.assertIn(u2_url, res_visible_to)



    # TODO: Test get post by invalid id

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
        # TODO: remove serializer.data
        data = {'comment': {'comment': 'my new comment', 'author': serializer.data}}
        request = self.factory.post(url, data=data, format='json')
        view = CommentViewList.as_view()
        force_authenticate(request, user=user)
        response = view(request, post_id=post.id)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['success'], True)
        self.assertEqual(response.data['message'], 'Comment Added')

    # test if user can comment on someone elses post
    def test_create_valid_other_comment(self):
        user1 = self.helper_functions.create_user()
        user2 = self.helper_functions.create_user(username="test2", email="test2@gmail.com")

        post = self.helper_functions.create_post(user1)
        url = reverse('comments', args=[post.id])

        serializer = UserSerializer(instance=user2)
        # print(serializer.data)

        comment_text = "My name is test2 and I am commenting"
        # TODO: remove serializer.data
        data = {'comment': {'comment': comment_text, 'author': serializer.data}}
        request = self.factory.post(url, data=data, format='json')
        view = CommentViewList.as_view()
        force_authenticate(request, user=user2)
        response = view(request, post_id=post.id)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['success'], True)
        self.assertEqual(response.data['message'], 'Comment Added')

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

class FollowTests(APITestCase):

    def setUp(self):
        self.factory = APIRequestFactory()
        self.helper_functions = GeneralFunctions()

    def get_follow_request(self, user, other):
        try:
            return FollowRequest.objects.get(requester=self.get_ww_user(user), requestee=self.get_ww_user(other))
        except FollowRequest.DoesNotExist:
            return None

    def get_follow(self, user, other):
        try:
            follow = Follow.objects.get(follower=self.get_ww_user(user), followee=self.get_ww_user(other))
        except Follow.DoesNotExist:
            return None

    def get_ww_user(self, user):
        try:
            return WWUser.objects.get(user_id=user.id)
        except WWUser.DoesNotExist:
            return None

    def populate_friends(self, numUsers):
        users = []
        names = ["alice%s" % s for s in range(numUsers)]
        users.append(self.helper_functions.create_user(username=names[0]))
        for x in range(1, numUsers):
            users.append(self.helper_functions.create_user(username=names[x]))
            self.helper_functions.create_follow(user=users[0], followee=users[x])
            self.helper_functions.create_follow(user=users[x], followee=users[0])
        return users

    def test_friend_request_non_follow(self):
        # friend request to user who doesn't follow requester
        user = self.helper_functions.create_user(username="Thom")
        other = self.helper_functions.create_user(username="Jessica")
        userSerializer = UserSerializer(instance=user)
        followSerializer = UserSerializer(instance=other)

        url = reverse('friendrequest')
        data = {"query": "friendrequest",
                "author": userSerializer.data,
                "friend": followSerializer.data
                }
        request = self.factory.post(url, data=data, format='json')
        view = FriendRequestView.as_view()
        force_authenticate(request, user=user)
        response = view(request)

        follow = FollowSerializer(
            Follow.objects.get(follower_id=userSerializer.data['id'], followee_id=followSerializer.data['id']))
        followRequest = FollowRequest.objects.get(requester=userSerializer.data.get('url'),
                                                  requestee=followSerializer.data.get('url'))
        self.assertIsNotNone(follow)
        self.assertIsNotNone(followRequest)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_friend_request_follow(self):
        # friend request to user who does follow requester
        user = self.helper_functions.create_user(username="Thom")
        other = self.helper_functions.create_user(username="Jessica")
        ww_user = WWUser.objects.get(user_id=user.id)
        ww_other = WWUser.objects.get(user_id=other.id)
        backwardFollow = Follow.objects.create(follower=ww_other, followee=ww_user)
        backwardFollow.save()
        userSerializer = UserSerializer(instance=user)
        followSerializer = UserSerializer(instance=other)

        url = reverse('friendrequest')
        data = {"query": "friendrequest",
                "author": userSerializer.data,
                "friend": followSerializer.data
                }

        request = self.factory.post(url, data=data, format='json')
        view = FriendRequestView.as_view()
        force_authenticate(request, user=user)
        response = view(request)
        follow = Follow.objects.get(follower=userSerializer.data['url'], followee=followSerializer.data['url'])
        followRequest = self.get_follow_request(user=user, other=other)
        self.assertIsNotNone(follow)
        self.assertIsNotNone(backwardFollow)
        self.assertIsNone(followRequest)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_friend_list(self):
        numFriends = 5
        users = self.populate_friends(numFriends)
        userSerializer = UserSerializer(instance=users, many=True)
        justaFollowee = self.helper_functions.create_user()
        self.helper_functions.create_follow(user=users[0], followee=justaFollowee)

        url = reverse('friendslist', args=[users[0].id])
        request = self.factory.get(url)
        view = FriendListView.as_view()
        response = view(request, pk=users[0].id)
        expectedResult = set([str(user.id) for user in users[1:]])

        # Verify we recieve 200 ok and the right list of uuids
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(set(response.data['authors']), set([str(user['id']) for user in userSerializer.data[1:]]))

    def test_friend_list_compare(self):
        numFriends = 5
        users = self.populate_friends(numFriends)
        justaFollowee = self.helper_functions.create_user()
        self.helper_functions.create_follow(user=users[0], followee=justaFollowee)
        # add a user who shouldn't be in the result list
        users.append(justaFollowee)

        url = reverse('friendslist', args=[users[0].id])
        data = {
            'query': 'friends',
            'author': users[0].id,
            'authors': [str(user.id) for user in users[1:]]
        }
        request = self.factory.post(url, data=data, format='json')
        view = FriendListView.as_view()
        response = view(request, pk=users[0].id)
        expectedResult = set([str(user.id) for user in users[1:-1]])

        # Verify we recieve 200 ok and the right list of uuids
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(set(response.data['authors']), set([str(user.id) for user in users[1:-1]]))

    def test_are_friends_yes(self):

        user1 = self.helper_functions.create_user(username="abram")
        user2 = self.helper_functions.create_user(username="hazel")
        self.helper_functions.create_follow(user=user1, followee=user2)
        self.helper_functions.create_follow(user=user2, followee=user1)

        url = reverse('arefriends', args=[user1.id, user2.id])
        request = self.factory.get(url)
        view = AreFriendsView.as_view()
        response = view(request, authorid1=user1.id, authorid2=user2.id)
        expectedResult = {
            'query': 'friends',
            'authors': [str(user1.id), str(user2.id)],
            'friends': True
        }

        # Verify we recieve 200 ok and the right list of uuids
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(set(response.data['authors']), set(expectedResult['authors']))
        self.assertEqual(response.data['query'], expectedResult['query'])
        self.assertEqual(response.data['friends'], expectedResult['friends'])

    def test_are_friends_no(self):
        # Even though these users are not friends, for the purpose
        # of this call, we are assuming peer 2 peer implementation
        # therefore it should be based on whether only whether
        # author 1 is following author 2, and the requestor needs
        # to check their endpoint for whether the other follow relation
        # exists.
        user1 = self.helper_functions.create_user(username="abram")
        user2 = self.helper_functions.create_user(username="hazel")
        self.helper_functions.create_follow(user=user1, followee=user2)

        url = reverse('arefriends', args=[user1.id, user2.id])
        request = self.factory.get(url)
        view = AreFriendsView.as_view()
        response = view(request, authorid1=user1.id, authorid2=user2.id)
        expectedResult = {
            'query': 'friends',
            'authors': [str(user1.id), str(user2.id)],
            'friends': True
        }

        # Verify we recieve 200 ok and the right list of uuids
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(set(response.data['authors']), set(expectedResult['authors']))
        self.assertEqual(response.data['query'], expectedResult['query'])
        self.assertEqual(response.data['friends'], expectedResult['friends'])

    def test_unfriend(self):

        user1 = self.helper_functions.create_user(username="abram")
        user2 = self.helper_functions.create_user(username="hazel")
        self.helper_functions.create_follow(user=user1, followee=user2)
        self.helper_functions.create_follow(user=user2, followee=user1)

        url = reverse('deletefollow', args=[user2.id])
        request = self.factory.delete(url)
        view = FollowView.as_view()
        force_authenticate(request, user=user1)
        response = view(request, authorid=user2.id)
        follow = self.get_follow(user=user1, other=user2)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertIsNone(follow)

    def test_unfriend_nonexistant(self):

        user1 = self.helper_functions.create_user(username="abram")
        user2 = self.helper_functions.create_user(username="hazel")
        self.helper_functions.create_follow(user=user2, followee=user1)

        url = reverse('deletefollow', args=[user2.id])
        request = self.factory.delete(url)
        view = FollowView.as_view()
        force_authenticate(request, user=user1)
        response = view(request, authorid=user2.id)
        follow = self.get_follow(user=user1, other=user2)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIsNone(follow)

    def test_follow_request_list(self):
        user1 = self.helper_functions.create_user(username="ada")
        user2 = self.helper_functions.create_user(username="church")
        user3 = self.helper_functions.create_user(username="alan")
        user1_serialized = UserSerializer(instance=user1)
        user2_serialized = UserSerializer(instance=user2)
        user3_serialized = UserSerializer(instance=user3)

        self.helper_functions.create_followrequest(user=user2, other=user1)
        self.helper_functions.create_followrequest(user=user3, other=user1)

        url = reverse('followereqlist')
        request = self.factory.get(url)
        view = FollowReqListView.as_view()
        force_authenticate(request, user=user1)
        response = view(request)
        expectedResult = {
            "query": "friendrequests",
            "author": user1_serialized.data['id'],
            "authors": [str(user2_serialized.data['id']), str(user3_serialized.data['id'])]
        }

        # Verify we recieve 204 ok and the right list of uuids
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(set(response.data['authors']), set(expectedResult['authors']))
        self.assertEqual(response.data['query'], expectedResult['query'])
        self.assertEqual(response.data['author'], expectedResult['author'])
