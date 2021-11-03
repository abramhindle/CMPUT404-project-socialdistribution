from django.db import models
from .authorModel import Author
from django.contrib.postgres.fields import ArrayField
import uuid


class Post(models.Model):
    ContentTypes = (
        ("text/plain", "Plain"),
        ("text/markdown", "Markdown"),
        ("application/base64", "Application"),
        ("image/png;base64", "ImagePNG"),
        ("image/jpeg;base64", "ImageJPEG")
    )

    VisibilityTypes = (
        ("PUBLIC", "public"),
        # ("PRIVATE", "Private"),
        # ("FOAF", "Friend of a Friend"),
        ("FRIENDS", "friends"),
        # ("SERVERONLY", "Server Only")
    )

    # Post ID 
    postID = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # Post url
    url = models.URLField(null=False)
    # Post origin url [contains the id of the original post/author]
    origin = models.URLField()
    # Post source url [tracks the source of the post]
    source = models.URLField()
    # Post author id
    postAuthorID = models.ForeignKey(Author, on_delete=models.CASCADE)
    # Post title
    title = models.TextField(max_length=150)
    # Post description
    description = models.CharField(max_length=300)
    # Post content(data)
    content = models.TextField() 
    # Post content type
    contentType = models.TextField(null=False, choices=ContentTypes, default='text/plain')
    # Post visibility status
    visibility = models.CharField(max_length=10, null=False, choices=VisibilityTypes, default='public')
    # Post published date
    published = models.DateTimeField(auto_now_add=True)
    # Post unlisted status
    unlisted = models.BooleanField(default=False)
    # Post category
    categories = ArrayField(models.CharField(max_length=100, blank=True), blank=True)
    # Post url name
    postURL = models.TextField()

    def visibilityStatus(self,friend=False):
        if self.visibility == "public" or self.visibility == "friends" and friend:
            return Author.objects.all()
        user = Author.objects.filter(id__exact=self.postAuthorID.authorID)
        return user

