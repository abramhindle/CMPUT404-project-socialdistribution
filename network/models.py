from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.contrib.postgres.fields import ArrayField
from django.dispatch import receiver
import uuid

class Author(models.Model):
    type = models.CharField(default='author', max_length=100)
    uuid = models.UUIDField(primary_key=True, null=False, default=uuid.uuid4, editable=False)
    id = models.URLField(null=True)
    url = models.URLField(null=True)
    host = models.URLField(null=True)
    displayName = models.CharField(null=True, max_length=100)
    github = models.URLField(null=True)
    profileImage = models.URLField(null=True)
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    # symmetrical=False allows Author to follow people that don't follow them
    followers = models.ManyToManyField("self", symmetrical=False, blank=True)

    def __init__(self, *args, **kwargs):
        super(Author, self).__init__(*args, **kwargs)
        if self.host != None:
            # make sure host ends with a '/'
            self.host += '/' if (not self.host.endswith('/')) else ''

            # set id and url to format specified in the project specifications
            self.id = self.host + self.type + '/' + str(self.uuid)
            self.url = self.id


# https://stackoverflow.com/a/52196396 to auto-create Author when User is created
@receiver(post_save, sender=User)
def create_user_author(sender, instance, created, **kwargs):
    if created:
        Author.objects.create(user=instance)
    instance.author.save()


class FriendRequest(models.Model):
    type = models.CharField(default='follow', max_length=100)
    summary = models.CharField(null=True, max_length=500)
    actor = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='actor')
    object = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='object')


class Post(models.Model):
    CONTENTCHOICES = (
        ("text/plain", "Plain"),
        ("text/markdown", "Markdown"),
        ("application/base64", "Base64"),
        ("image/png;base64", "PNG"),
        ("image/jpeg;base64", "JPEG")
    )

    VISIBILITY = (
        ("PUBLIC", "Public"),
        ("PRIVATE", "Private"),
        ("FOAF", "Friend of a Friend"),
        ("FRIENDS", "Friends"),
        ("SERVERONLY", "Server Only")
    )

    type = models.CharField(default='post', max_length=100)
    title = models.CharField(null=True, max_length=100)
    uuid = models.UUIDField(primary_key=True, null=False, default=uuid.uuid4, editable=False)
    id = models.URLField(null=True)
    source = models.URLField(null=True)
    origin = models.URLField(null=True)
    description = models.CharField(null=True, max_length=500)
    contentType = models.CharField(choices=CONTENTCHOICES, default="text/plain", max_length=20)
    content = models.TextField(null=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='post_author')
    image = models.ImageField(upload_to='users/%Y-%m-%d/', blank=True)
    categories = ArrayField(models.CharField(max_length=100), blank=True)
    count = models.IntegerField(null=True)
    comments = models.URLField(null=True)
    # commentsSrc = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='commentsSrc')
    published = models.DateTimeField(null=True, auto_now_add=True)
    visibility = models.CharField(max_length=10, choices=VISIBILITY, default="PUBLIC")
    unlisted = models.BooleanField(null=True)

    def __init__(self, *args, **kwargs):
        super(Post, self).__init__(*args, **kwargs)
        if self.author != None:
            # make sure host ends with a '/'
            self.author.id += '/' if (not self.author.id.endswith('/')) else ''

            # set id to format specified in the project specifications
            self.id = self.author.id + 'posts/' + str(self.uuid)

class Comment(models.Model):
    CONTENTCHOICES = (
        ("text/plain", "Plain"),
        ("text/markdown", "Markdown")
    )

    uuid = models.UUIDField(primary_key=True, null=False, default=uuid.uuid4, editable=False)
    id = models.URLField(null=True)
    type = models.CharField(default='comment', max_length=50)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='comment_author')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comment_post')
    comment = models.CharField(max_length=1024)
    contentType = models.CharField(max_length=18, choices=CONTENTCHOICES, default="text/plain")
    published = models.DateTimeField(null=True, auto_now_add=True)

    def __init__(self, *args, **kwargs):
        super(Comment, self).__init__(*args, **kwargs)
        if self.post != None:
            # make sure host ends with a '/'
            self.post.id += '/' if (not self.post.id.endswith('/')) else ''

            # set id to format specified in the project specifications
            self.id = self.post.id + 'comments/' + str(self.uuid)

class Like(models.Model):
    context = models.CharField(default='https://www.w3.org/ns/activitystreams', max_length=100)
    summary = models.CharField(null=True, max_length=500)
    type = models.CharField(default='like', max_length=100)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='like_author')
    object = models.URLField(null=True)
    date = models.DateTimeField(auto_now=True)


class CustomUser(User):
    # Any extra fields would go here
    def __str__(self):
        return self.email, self.username




class temp(models.Model):
    displayName = models.CharField(null=True, max_length=100)
   