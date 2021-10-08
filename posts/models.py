import uuid
from django.db import models
from authors.models import Author
from django.utils.translation import gettext_lazy as _
from django.urls import reverse 
from django.contrib.postgres import fields

class Post(models.Model):
    # https://docs.djangoproject.com/en/3.2/ref/models/fields/#enumeration-types
    class ContentType(models.TextChoices):
        MARKDOWN = 'MDN', _('text/markdown')
        PLAIN = 'PLN', _('text/plain')
        APPLICATION = 'APP', _('application/base64')
        IMAGE_PNG = 'PNG', _('image/png;base64')
        IMAGE_JPEG = 'JPG', _('image/jpeg;base64')

    class Visibility(models.TextChoices):
        PUBLIC = 'PUB', _('PUBLIC')
        FRIENDS = 'FRI', _('FRIENDS')
        PRIVATE = 'PRI', _('PRIVATE')

    id = models.CharField(primary_key=True, editable=False, max_length=40, default=uuid.uuid4)
    url = models.URLField(editable=False)
    author = models.ForeignKey(Author, related_name="post", on_delete=models.CASCADE)
    
    title = models.CharField(max_length=30) # title should not be super long
    source = models.URLField(editable=False)
    origin = models.URLField(editable=False)
    description = models.CharField(max_length = 50)
    content_type = models.CharField(max_length=3, choices=ContentType.choices, default=ContentType.PLAIN)
    content = models.TextField()
    published = models.DateTimeField(auto_now_add=True)
    unlisted = models.BooleanField(default=False)
    visibility = models.CharField(max_length=3, choices=Visibility.choices, default=Visibility.PUBLIC)

    # TODO: As an author, posts I create can link to images.
    # TODO: As an author, posts I create can be images..

    # make the admin page looks pretty
    def __str__(self):
        return self.title + " (" + str(self.id) + ")"

    # This will return the label of the enum (e.g. "PUBLIC")
    # instead of the value of the enum (e.g. "PUB")
    def get_visilibility_label(self):
        return self.Visibility(self.visibility).label

    def get_content_type_label(self):
        return self.ContentType(self.content_type).label

    # used by serializer
    def get_public_id(self):
        return self.url or self.id

    def get_api_type(self):
        return 'post'

    # used internally
    def get_absolute_url(self):
        return reverse('post-detail', args=[str(self.author.id), str(self.id)])

    def count_comments(self):
        return self.comment_set.count()

    # used by serializer
    def update_fields_with_request(self, request):
        self.url = request.build_absolute_uri(self.get_absolute_url())
        self.host = request.build_absolute_uri('/') # points to the server root
        self.save()

class Comment(models.Model):
    id = models.CharField(primary_key=True, editable=False, max_length=40, default=uuid.uuid4)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    comment = models.TextField()
    published = models.DateTimeField()

    # TODO: question: should comments supports the same content-types as posts?
    # content_type = ?

class Like(models.Model):
    summary = models.CharField(max_length=30)
    author = models.ForeignKey(Author, related_name = "likes", on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name = "likes", on_delete=models.CASCADE)

    # https://docs.djangoproject.com/en/3.2/ref/models/constraints/#django.db.models.UniqueConstraint
    class Meta:
        # ensure one author can only like a post once
        constraints = [
            models.UniqueConstraint(fields=['author', 'post'], name='unique_like')
        ]