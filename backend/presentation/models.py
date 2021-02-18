from django.db import models

VISIBILILTY_CHOICES = [
    ('PUBLIC', 'PUBLIC'),
    ('FRIENDS', 'FRIENDS'),
]


class Author(models.Model):
    type = "author"
    authorID = models.URLField(max_length=200)
    host = models.URLField(max_length=200)  # the home host of the author
    # the display name of the author
    displayName = models.CharField(max_length=50)
    url = models.URLField(max_length=200)  # url to the authors profile
    github = models.URLField(max_length=200)  # HATEOS url for Github API


class Follower(models.Model):
    type = "followers"
    list = models.ManyToManyField(
        Author,
        blank=True,
        related_name='follower_list')  # contain Author Objects


class Comment(models.Model):
    type = "comment"
    author = models.ForeignKey(
        "Author", on_delete=models.CASCADE, related_name="comment_author")
    comment = models.TextField()
    contentType = models.CharField(max_length=50)
    published = models.DateField(auto_now=False, auto_now_add=False)
    commentID = models.URLField(max_length=200)


class Post(models.Model):
    type = "post"
    title = models.CharField(max_length=50)
    postID = models.URLField(max_length=200)
    source = models.URLField(max_length=200)
    origin = models.URLField(max_length=200)
    description = models.CharField(max_length=100)
    contentType = models.CharField(max_length=50)
    content = models.TextField()
    author = models.ForeignKey(
        Author, on_delete=models.CASCADE, related_name="post_author")
    categories = models.TextField()  # a list of string
    count = models.IntegerField()
    size = models.IntegerField()
    comment = models.URLField(max_length=200)
    comments = models.ManyToManyField(
        Comment,
        blank=True, related_name="post_comments")  # contain Comment Objects
    published = models.DateField(
        auto_now=False, auto_now_add=False)  # ISO 8601 TIMESTAMP
    visibility = models.CharField(
        max_length=50, choices=VISIBILILTY_CHOICES, default='PUBLIC')
    # unlisted means it is public if you know the post name -- use this for images, it's so images don't show up in timelines
    unlisted = models.BooleanField()


class Request(models.Model):
    type = "Follow"
    summary = models.CharField(max_length=50)
    actor = models.ForeignKey(
        "Author", on_delete=models.CASCADE, related_name="request_author")
    object = models.ForeignKey(
        "Author", on_delete=models.CASCADE, related_name="request_object")


class Inbox(models.Model):
    type = "inbox"
    author = models.URLField(max_length=200)
    items = models.ManyToManyField(
        Post,
        blank=True, related_name="inbox_items")  # contain Post objects


class Likes(models.Model):
    type = "Like"
    context = models.URLField(max_length=200)  # @context?
    summary = models.CharField(max_length=50)
    author = models.ForeignKey(
        "Author", on_delete=models.CASCADE, related_name="likes_author")
    object = models.URLField(max_length=200)


class Liked(models.Model):
    type = "liked"
    items = models.ManyToManyField(
        Likes,
        blank=True, related_name="liked_items")  # contain Likes Objects
