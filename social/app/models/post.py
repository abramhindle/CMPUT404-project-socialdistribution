import uuid

import CommonMark
from django.db import models
from django.urls import reverse

from social.app.models.author import Author
from social.app.models.category import Category


class Post(models.Model):
    # Code idea from Django Docs,
    # url: https://docs.djangoproject.com/en/dev/ref/models/fields/#choices
    TEXT_CONTENT_TYPES = [
        ("text/markdown", "Markdown"),
        ("text/plain", "Plain Text"),
    ]

    FILE_CONTENT_TYPES = [
        ("application/base64", "File Upload"),
        ("image/png;base64", "Image (PNG)"),
        ("image/jpeg;base64", "Image (JPEG)"),
    ]

    CONTENT_TYPES = TEXT_CONTENT_TYPES + FILE_CONTENT_TYPES

    VISIBILITY_OPTIONS = [
        ("PUBLIC", "Public"),
        ("FOAF", "FOAF"),
        ("FRIENDS", "Friends"),
        ("PRIVATE", "Private"),
        ("SERVERONLY", "This Server Only"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.TextField()
    source = models.URLField()
    origin = models.URLField()
    description = models.TextField()

    content_type = models.CharField(
        max_length=20,
        choices=CONTENT_TYPES,
        default="text/plain"
    )

    content = models.TextField(default="")

    author = models.ForeignKey(
        Author,
        on_delete=models.CASCADE
    )

    categories = models.ManyToManyField(
        Category,
        blank=True
    )

    published = models.DateTimeField(auto_now_add=True)

    visibility = models.CharField(
        max_length=10,
        choices=VISIBILITY_OPTIONS,
        default="PUBLIC",
    )

    # List of Authors who can read the PRIVATE message
    # attribute only renders in /posts/add/ if visibility is set to "PRIVATE"
    visible_to = models.ManyToManyField(
        Author,
        related_name='visible_posts',
        blank=True
    )

    unlisted = models.BooleanField(default=False)

    def get_absolute_url(self):
        """
        Add new posts to database
        """
        return reverse('app:posts:detail', kwargs={'pk': self.id})

    def content_html(self):
        if self.content_type == "text/plain":
            return self.content
        if self.content_type == "text/markdown":
            parser = CommonMark.Parser()
            renderer = CommonMark.HtmlRenderer(options={'safe': True})
            return renderer.render(parser.parse(self.content))

        return ""

    def categories_string(self):
        names = [cat.name for cat in self.categories.all()]
        if names:
            return " ".join(names)

        return ""

