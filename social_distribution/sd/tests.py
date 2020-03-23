from django.test import TestCase
from django.urls import resolve
from unittest import skip

from sd.models import *
from sd.views import *


class ModelTests(TestCase):
    def create_author(self, first_name="Test", last_name="Author", bio="I am a test author"):
        return Author(
            first_name = first_name,
            last_name = last_name,
            bio = "I am a test author"
        )

    def create_post(self, author=None, title="test post", content="this is a test", visibility=1, link_to_image=""):
        a = author if author != None else self.create_author()

        return Post(
            contentType = 2,
            author = a,
            title = title,
            content = content,
            visibility = visibility,
            link_to_image = link_to_image,
        )

    def create_comment(self, author, post, comment="comment"):
        return Comment(
            author = author,
            comment = comment,
            contentType = 2,
            post = post
        )

    def create_friend_request(self, to, fr):
        return FriendRequest(
            to_author = to,
            from_author = fr
        )

    def create_follow(self, following, follower):
        return Follow(
            following = following,
            follower = follower
        )

    def create_friend(self, current, friend):
        return Friend(
            author = current,
            friend = friend
        )

    def test_author(self):
        a = self.create_author()
        self.assertTrue(isinstance(a, Author))

        self.assertEqual(a.first_name, "Test")
        self.assertEqual(a.last_name, "Author")
        self.assertEqual(a.bio, "I am a test author")

    def test_post(self):
        p = self.create_post()
        self.assertTrue(isinstance(p, Post))
        self.assertTrue(isinstance(p.author, Author))

        self.assertEqual(p.title, "test post")
        self.assertEqual(p.content, "this is a test")
        self.assertEqual(p.visibility, 1)
        self.assertEqual(p.link_to_image, "")

        self.assertEqual(p.author.first_name, "Test")
        self.assertEqual(p.author.last_name, "Author")
        self.assertEqual(p.author.bio, "I am a test author")

    def test_comment(self):
        a = self.create_author(first_name="Justan", last_name="Author")
        a2 = self.create_author(first_name="Makea", last_name="Post")
        p = self.create_post(author=a2)

        c = self.create_comment(a, p)

        self.assertTrue(isinstance(c, Comment))
        self.assertEqual(c.author, a)
        self.assertEqual(c.post, p)

        self.assertEqual(c.comment, "comment")

    def test_friend_request(self):
        a1 = self.create_author(first_name="To", last_name="Me")
        a2 = self.create_author(first_name="From", last_name="Me")

        fr = self.create_friend_request(a1, a2)

        self.assertTrue(isinstance(fr, FriendRequest))
        self.assertEqual(a1, fr.to_author)
        self.assertEqual(a2, fr.from_author)

    def test_follow(self):
        a1 = self.create_author(first_name="Follow", last_name="Ing")
        a2 = self.create_author(first_name="Follow", last_name="Er")

        f = self.create_follow(a1, a2)

        self.assertTrue(isinstance(f, Follow))
        self.assertEqual(a1, f.following)
        self.assertEqual(a2, f.follower)

    def test_friend(self):
        a1 = self.create_author(first_name="Current", last_name="Auth")
        a2 = self.create_author(first_name="Friend", last_name="Auth")

        fr = self.create_friend(a1, a2)

        self.assertTrue(isinstance(fr, Friend))
        self.assertEqual(a1, fr.author)
        self.assertEqual(a2, fr.friend)

class URLTests(TestCase):
    def test_get_login(self):
        r = resolve('/login')
        self.assertEqual(r.func, login)

    def test_get_login(self):
        r = resolve('/logout/')
        self.assertEqual(r.func, logout)

    def test_get_register(self):
        r = resolve('/register/')
        self.assertEqual(r.func, register)

    def test_get_newpost(self):
        r = resolve('/newpost')
        self.assertEqual(r.func, new_post)

    @skip("Not implemented")
    def test_get_requests(self):
        r = resolve('/requests')
        self.assertEqual(r.func, requests)

    def test_get_notifications(self):
        r = resolve('/notifications')
        self.assertEqual(r.func, notifications)

    def test_get_my_feed(self):
        r = resolve('/feed')
        self.assertEqual(r.func, feed)

    def test_get_account(self):
        r = resolve('/account')
        self.assertEqual(r.func, account)

    def test_get_search(self):
        r = resolve('/search')
        self.assertEqual(r.func, search)

    @skip("This page doesn't exist right now")
    def test_get_author_posts(self):
        r = resolve('/author/posts')
        self.assertEqual(r.func, feed)

    @skip("IDs aren't working yet")
    def test_get_author_id_posts(self):
        r = resolve('/author/1/posts')
        self.assertEqual(r.func, author)

    @skip("IDs aren't working yet")
    def test_get_post_id(self):
        r = resolve('/posts/1')
        self.assertEqual(r.func, post)

    @skip("IDs aren't working yet")
    def test_get_post_id_comments(self):
        r = resolve('/post/1/comments')
        self.assertEqual(r.func, post_comment)

    @skip("IDs aren't working yet")
    def test_get_author_id_friends(self):
        r = resolve('/author/1/friends')
        self.assertEqual(r.func, friends)

class BasicActions(TestCase):

    def setUp(self):
        pass

    def test_edit_post(self):
        pass

    def test_delete_post(self):
        pass

    def test_edit_not_my_post(self):
        pass

    def test_delete_not_my_post(self):
        pass

    def test_create_plaintext_post(self):
        pass

    def test_create_markdown_post(self):
        pass

    def test_cant_comment_on_post(self):
        pass

    def test_post_with_image(self):
        pass

    def test_access_image_no_auth(self):
        pass

    def test_view_public_posts(self):
        pass

class FriendsTestCases(TestCase):
    def setUp(self):
        pass

    def test_render_friend_post(self):
        pass

    def test_send_friend_request(self):
        pass

    def test_receive_friend_request(self):
        pass

    def test_post_from_not_friend(self):
        pass

    def test_create_unlisted_post(self):
        pass

    def test_create_private_post(self):
        pass

    def test_create_private_to_friends_post(self):
        pass

    def test_creat_foaf_post(self):
        # post is only visible to friend of a friend
        pass

    def test_create_public_post(self):
        pass

    def test_unfriend_local(self):
        pass

    def test_unfriend_remote(self):
        pass

class ServerTests(TestCase):
    def setUp(self):
        pass

    def test_host_images(self):
        pass

    def test_add_author(self):
        pass

    def test_modify_author(self):
        pass

    def test_remove_author(self):
        pass

    def test_allow_new_user(self):
        pass

    def test_setup_not_approved(self):
        # As a user who signed up but hasn't been approved by the server,
        # I shouldn't be able to do anything
        pass

    def test_add_remote_server_with_auth(self):
        pass

    def test_add_remote_server_no_auth(self):
        # This shouldn't work
        pass

    def test_disable_remote_server_conn(self):
        pass

    def test_share_posts_across_server(self):
        pass

    def test_no_share_posts_across_server(self):
        pass
