from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from posts.models import Post, Category
from django.urls import reverse

from .constants import POST_DATA

EDITED_POST_DATA = POST_DATA.copy()
EDITED_POST_DATA['content_type'] = Post.ContentType.MARKDOWN


class CreatePostTests(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        get_user_model().objects.create_user(username='bob', password='password')

    def test_new_post_page(self):
        self.client.login(username='bob', password='password')
        res = self.client.get(reverse('posts:new'))
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed('posts/create_post.html')

    def test_new_post_require_login(self):
        res = self.client.get(reverse('posts:new'))
        self.assertEqual(res.status_code, 302)

    def test_new_post_require_csrf(self):
        csrf_client = Client(enforce_csrf_checks=True)
        csrf_client.login(username='bob', password='password')
        res = csrf_client.post(reverse('posts:new'), data=POST_DATA)
        self.assertEqual(res.status_code, 403)

    def test_new_post(self):
        self.client.login(username='bob', password='password')
        initial_post_count = len(Post.objects.all())
        self.client.post(reverse('posts:new'), data=POST_DATA)
        self.assertEqual(len(Post.objects.all()), initial_post_count + 1)

    def test_categories_not_duplicated(self):
        self.client.login(username='bob', password='password')
        Category.objects.create(category='web')
        initial_post_count = len(Post.objects.all())
        self.client.post(reverse('posts:new'), data=POST_DATA)
        self.assertEqual(len(Category.objects.all()), 2)
        self.assertEqual(len(Post.objects.all()), initial_post_count + 1)


class EditPostTests(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        current_user = 'bob'
        get_user_model().objects.create_user(username=current_user, password='password')

        # Create test post to edit
        post = Post.objects.create(
            title=POST_DATA['title'],
            description=POST_DATA['description'],
            content_type=POST_DATA['content_type'],
            content=POST_DATA['content'],
            author_id=get_user_model().objects.get(
                username=current_user).id,
            unlisted=True)
        post.save()
        self.post_id = post.id

    def test_edit_post_page(self):
        self.client.login(username='bob', password='password')
        res = self.client.get(reverse('posts:edit', kwargs={'pk': self.post_id}))
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed('posts/edit_post.html')

    def test_edit_post_require_login(self):
        res = self.client.get(reverse('posts:edit', kwargs={'pk': self.post_id}))
        self.assertEqual(res.status_code, 302)

    def test_edit_post_require_csrf(self):
        csrf_client = Client(enforce_csrf_checks=True)
        csrf_client.login(username='bob', password='password')
        res = csrf_client.post(reverse('posts:edit', kwargs={'pk': self.post_id}), data=EDITED_POST_DATA)
        self.assertEqual(res.status_code, 403)

    def test_edit_post(self):
        self.client.login(username='bob', password='password')
        res = self.client.post(reverse('posts:edit', kwargs={'pk': self.post_id}), data=EDITED_POST_DATA)
        self.assertEqual(res.status_code, 302)
        self.assertEqual(Post.objects.get(pk=self.post_id).content_type, EDITED_POST_DATA['content_type'])

    def test_edit_non_existing_post(self):
        self.client.login(username='bob', password='password')
        res = self.client.post(reverse('posts:edit', kwargs={'pk': 900}), data=EDITED_POST_DATA)
        self.assertEqual(res.status_code, 404)
