from django.test import TestCase

class UITestCases(TestCase):
    def setUp(self):
        pass

    def test_render_home_page(self):
        pass

    def test_render_post(self):
        pass

    def test_view_profile(self):
        pass


class BasicActions(TestCase):
    def setUp(self):
        pass

    def test_make_post(self):
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