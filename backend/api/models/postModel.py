from django.db import models
from .authorModel import Author
from django.contrib.postgres.fields import ArrayField
import uuid

class Post(models.Model):
    TEXT_PLAIN = "text/plain"
    TEXT_MARKDOWN = "text/markdown"
    APPLICATION_BASE64 = "application/base64"
    IMAGE_PNG = "image/png;base64"
    IMAGE_JPEG = "image/jpeg;base64"

    ContentTypes = (
        (TEXT_PLAIN, "Plain"),
        (TEXT_MARKDOWN, "Markdown"),
        (APPLICATION_BASE64, "Application"),
        (IMAGE_PNG, "ImagePNG"),
        (IMAGE_JPEG, "ImageJPEG")
    )

    PUBLIC = "PUBLIC"
    PRIVATE = "PRIVATE"

    VisibilityTypes = (
        (PUBLIC, "public"),
        (PRIVATE, "friends")
    )

    # Post Type
    type = models.CharField(default='post', max_length=100)
    # Post Title
    title = models.TextField(default='post title', max_length=150)
    # Post UUID 
    uuid = models.UUIDField(primary_key=True, null=False, default=uuid.uuid4, editable=False)
    # Post ID 
    id = models.URLField(null=True, blank=True)
    # Post Source (tracks where the post was gotten from)
    source = models.URLField(null=True, blank=True)
    # Post Origin (tracks where the post is actually from)
    origin = models.URLField(null=True, blank=True)
    # Post Description
    description = models.CharField(null=True, blank=True, max_length=300)
    # Post Content Type
    contentType = models.CharField(null=False, choices=ContentTypes, default=TEXT_PLAIN, max_length=20)
    # Post Content (could be empty if the post is just an image)
    content = models.TextField(null=True, blank=True) 
    # Post Author
    author = models.ForeignKey(Author, on_delete=models.CASCADE, null=True, related_name='post_author')
    # Post Image
    image = models.ImageField(upload_to='users/%Y-%m-%d/', null=True, blank=True)
    # Post Categories
    categories = ArrayField(models.CharField(max_length=100, null=True, blank=True), null=True, blank=True)
    # Total Number of Comments for the Post
    count = models.IntegerField(null=True, blank=True)
    # Link to Comments for the Post
    comments = models.URLField(null=True, blank=True)
    # Post Published Date
    published = models.DateTimeField(null=True, blank=True, auto_now_add=True)
    # Post Visibility Status
    visibility = models.CharField(max_length=10, null=False, choices=VisibilityTypes, default=PUBLIC)
    # Post Unlisted Status
    unlisted = models.BooleanField(default=False)

    def __init__(self, *args, **kwargs):
        super(Post, self).__init__(*args, **kwargs)
        if self.author != None:
            # make sure host ends with a '/'
            self.author.id += '/' if (not self.author.id.endswith('/')) else ''

            # set id to format specified in the project specifications
            self.id = self.author.id + 'posts/' + str(self.uuid)

            # set comments to format specified in the project specifications
            self.comments = self.id + '/comments'

    def visibilityStatus(self, friend=False):
        if self.visibility == "public" or self.visibility == "friends" and friend:
            return Author.objects.all()
        user = Author.objects.filter(id__exact=self.postAuthorID.authorID)
        return user
