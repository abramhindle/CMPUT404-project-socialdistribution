from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from posts.models import Post, Category, ContentType, Comment, Like
from django.urls import reverse

from .constants import COMMENT_DATA, POST_DATA

EDITED_POST_DATA = POST_DATA.copy()
EDITED_POST_DATA['content_type'] = ContentType.MARKDOWN


class CreatePostViewTests(TestCase):
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


class EditPostViewTests(TestCase):
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


class PostDetailViewTests(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.user = get_user_model().objects.create_user(username='bob', password='password')
        self.post = Post.objects.create(
            title=POST_DATA['title'],
            description=POST_DATA['description'],
            content_type=POST_DATA['content_type'],
            content=POST_DATA['content'],
            author_id=self.user.id,
            unlisted=True)
        self.post.save()

    def test_detail_view_page(self):
        self.client.login(username='bob', password='password')
        res = self.client.get(reverse('posts:detail', kwargs={'pk': self.post.id}))
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'posts/post_detail.html')
        self.assertContains(res, self.post.title)
        self.assertContains(res, self.post.author.get_full_name())
        self.assertContains(res, self.post.content)
        for category in self.post.categories.all():
            self.assertContains(res, category.category)

    def test_comments_section(self):
        for _ in range(3):
            comment = Comment.objects.create(
                comment=COMMENT_DATA['comment'],
                author=self.user,
                content_type=COMMENT_DATA['content_type'],
                post=self.post,
            )
            comment.save()

        self.client.login(username='bob', password='password')
        res = self.client.get(reverse('posts:detail', kwargs={'pk': self.post.id}))
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, 'Comments')
        self.assertContains(res, COMMENT_DATA['comment'], count=3)

    def test_like_section(self):
        self.client.login(username='bob', password='password')
        res = self.client.get(reverse('posts:detail', kwargs={'pk': self.post.id}))
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, 'Like')

    def test_like(self):
        self.client.login(username='bob', password='password')
        res = self.client.post(reverse('posts:like', kwargs={'pk': self.post.id}))
        self.assertEqual(res.status_code, 302)
        self.assertIsNotNone(Like.objects.get(author=self.user, post=self.post))

    def test_like_require_csrf(self):
        csrf_client = Client(enforce_csrf_checks=True)
        csrf_client.login(username='bob', password='password')
        res = csrf_client.post(reverse('posts:like', kwargs={'pk': self.post.id}))
        self.assertEqual(res.status_code, 403)

    def test_disable_like(self):
        Like.objects.create(author=self.user, post=self.post)
        self.client.login(username='bob', password='password')
        res = self.client.get(reverse('posts:detail', kwargs={'pk': self.post.id}))
        self.assertEqual(res.status_code, 200)
        self.assertNotContains(res, 'Like')


class PostDeleteViewTests(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.user = get_user_model().objects.create_user(username='bob', password='password')
        self.post = Post.objects.create(
            title=POST_DATA['title'],
            description=POST_DATA['description'],
            content_type=POST_DATA['content_type'],
            content=POST_DATA['content'],
            author_id=self.user.id,
            unlisted=True)
        self.post.save()

    def test_post_delete_view_page(self):
        self.client.login(username='bob', password='password')
        res = self.client.get(reverse('posts:delete', kwargs={'pk': self.post.id}))
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'posts/delete_post.html')
        self.assertContains(res, self.post.title)

    def test_post_delete_view(self):
        initial_post_count = len(Post.objects.all())
        self.client.login(username='bob', password='password')
        res = self.client.post(reverse('posts:delete', kwargs={'pk': self.post.id}))
        self.assertEqual(res.status_code, 302)
        self.assertEqual(len(Post.objects.all()), initial_post_count - 1)


class CreateCommentViewTests(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.user = get_user_model().objects.create_user(username='bob', password='password')
        self.post = Post.objects.create(
            title=POST_DATA['title'],
            description=POST_DATA['description'],
            content_type=POST_DATA['content_type'],
            content=POST_DATA['content'],
            author_id=self.user.id,
            unlisted=True)
        self.post.save()

    def test_new_comment_page(self):
        self.client.login(username='bob', password='password')
        res = self.client.get(reverse('posts:new-comment', kwargs={'pk': self.post.id}))
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'comments/create_comment.html')

    def test_new_comment(self):
        self.client.login(username='bob', password='password')
        res = self.client.post(reverse('posts:new-comment', kwargs={'pk': self.post.id}), data=COMMENT_DATA)
        self.assertEqual(res.status_code, 302)
        self.assertRedirects(res, reverse('posts:detail', kwargs={'pk': self.post.id}))
        self.assertEqual(len(self.post.comment_set.all()), 1)

    def test_new_comment_require_login(self):
        res = self.client.get(reverse('posts:edit', kwargs={'pk': self.post.id}))
        self.assertEqual(res.status_code, 302)

    def test_new_comment_require_csrf(self):
        csrf_client = Client(enforce_csrf_checks=True)
        csrf_client.login(username='bob', password='password')
        res = csrf_client.post(reverse('posts:new-comment', kwargs={'pk': self.post.id}), data=COMMENT_DATA)
        self.assertEqual(res.status_code, 403)


class MyPostsViewTests(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.user = get_user_model().objects.create_user(username='bob', password='password')
        alice = get_user_model().objects.create_user(username='alice', password='password')
        self.posts: list[Post] = []
        self.posts_per_user = 2

        for user in [self.user, alice]:
            for _ in range(self.posts_per_user):
                post = Post.objects.create(
                    title=POST_DATA['title'],
                    description=POST_DATA['description'],
                    content_type=POST_DATA['content_type'],
                    content=POST_DATA['content'],
                    author_id=user.id,
                    unlisted=True)
                post.save()

    def test_post_list_page(self):
        self.client.login(username='bob', password='password')
        res = self.client.get(reverse('posts:my-posts'))
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'posts/post_list.html')

    def test_post_list_empty_page(self):
        Post.objects.filter(author=self.user).delete()
        self.client.login(username='bob', password='password')
        res = self.client.get(reverse('posts:my-posts'))
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, 'No posts yet')

    def test_post_list(self):
        self.client.login(username='bob', password='password')
        res = self.client.get(reverse('posts:my-posts'))
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, POST_DATA['title'], self.posts_per_user)

    def test_new_comment_require_login(self):
        res = self.client.get(reverse('posts:my-posts'))
        self.assertEqual(res.status_code, 302)
