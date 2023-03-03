from django.db import models

# Create your models here.
from django.urls import reverse
from apps.authors.models import Author
# Create your models here.


class Post(models.Model):

    # Fields
    id = models.CharField(primary_key=True, max_length=255)
    title = models.CharField(max_length=250, blank=True)
    source = models.CharField(max_length=50, blank=True)
    origin = models.CharField(max_length=50, blank=True)
    description = models.CharField(max_length=250, blank=True)

    CONTENT_CHOICES = (
        ("text/markdown", "text/markdown"),
        ("plain/Text", "plain/Text"),
    )
    contentType = models.CharField(
        choices=CONTENT_CHOICES, max_length=20, blank=True)
    author_id = models.ForeignKey(Author, on_delete=models.CASCADE)

    def commentlist_template():
        return {"comment_id": "[]"}

    def category_template():
        return {"category": "[]"}
    categories = models.JSONField(blank=True, default=category_template)
    comments = models.JSONField(
        blank=True, verbose_name='comment', default=commentlist_template)

    count = models.PositiveBigIntegerField(default=0)
    published = models.DateTimeField(auto_now_add=True)
    VISIBIILTY_CHOICES = (
        (True, "PUBLIC"),
        (False, "PRIVATE"),
    )
    visibility = models.BooleanField(
        choices=VISIBIILTY_CHOICES, default=True)
    image = models.ImageField(blank=True, null=True)
    unlisted = models.BooleanField(blank=True, default=False)

    def get_like(self):
        return self.count

    def increment_like(self):
        self.count = self.count + 1

    def get_id(self):
        return self.id

    def get_root_comments(self):
        """The plan is to call a function from the comment class and then get it here."""
        pass

    def __str__(self):
        return self.title


class Comment(models.Model):
    id = models.CharField(primary_key=True, max_length=255)
    url = models.URLField(max_length=250)
    host = models.CharField(max_length=100, blank=True)
    displayName = models.CharField(max_length=200)
    message: models.CharField(max_length=250)
    parent_post_id = models.ForeignKey(
        Post, on_delete=models.CASCADE, blank=True, null=True)
    profileImage = models.ImageField(blank=True)
    parent_comment_id = models.BigIntegerField(blank=True, null=True)

    def get_comment_id(self):
        return self.id

    def __str__(self):
        self.message


class Friend(models.Model):
    """
    Each individual record is a someone following someone. So, all the following/Friend
    info is here.
    follower is the id of the author who is following.
    owner is the id of the author who is being followed.
    """
    id = models.CharField(primary_key=True, max_length=255)
    followers = models.ForeignKey(
        Author, on_delete=models.CASCADE, related_name='follower')
    dateTime = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(
        Author, on_delete=models.CASCADE, related_name='owner')


class Inbox(models.Model):
    """
    Here the author is the id of the author whos inbox is this
    Post is the post sent to the person's inbox. Pretty straightforward. 
    """
    id = models.CharField(primary_key=True, max_length=255)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    dateTime = models.DateTimeField(auto_now_add=True)
