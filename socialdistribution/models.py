from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.postgres.fields import ArrayField
from django.conf import settings
import uuid


def uuid_hex():
    return uuid.uuid4().hex

class Author(AbstractUser):
    # model for author
    email = models.EmailField(max_length=60, unique=True)
    username = models.CharField(max_length=30)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    authorID = models.CharField(unique=True, default=uuid_hex, editable=False, max_length=40)
    github = models.URLField(max_length=200, blank=True)

    USERNAME_FIELD = 'email' # use email to login
    REQUIRED_FIELDS = ['username']

    def get_id(self):
        return settings.HOST_URL + "author/" + self.authorID

    def get_host(self):
        return settings.HOST_URL

    def get_type(self):
        return "author"

class Post(models.Model):
    title = models.CharField(max_length=200)
    postID = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True)
    source = models.URLField(max_length=200)
    origin = models.URLField(max_length=200)
    description = models.TextField()
    contentType = models.CharField(max_length=20, default="text/plain")
    content = models.TextField()
    authorID = models.CharField(max_length=40)
    # categories
    count = models.IntegerField(default=0)
    # comments
    comment_list = ArrayField(models.JSONField(), default=list)

    # comments dict
    published = models.DateTimeField(auto_now_add=True)
    visibility = models.CharField(max_length=10, default="PUBLIC")
    unlisted = models.BooleanField(default=False)

    def get_post_id(self):
        return "{}author/{}/posts/{}".format(settings.HOST_URL, self.authorID, str(self.postID))

    def get_comments_url(self):
        return self.get_post_id() + "/comments"

    def get_type(self):
        return "post"

# partially from https://briancaffey.github.io/2017/07/19/different-ways-to-build-friend-models-in-django.html/
class Follow(models.Model):
    users = models.ManyToManyField(Author)
    current_user = models.ForeignKey(Author, related_name="owner", null=True, on_delete=models.CASCADE)

    @classmethod
    def follow(cls, current_user, new_friend):
        friend, created = cls.objects.get_or_create(
            current_user = current_user
        )
        friend.users.add(new_friend)

    @classmethod
    def unfollow(cls, current_user, new_friend):
        friend, created = cls.objects.get_or_create(
            current_user = current_user
        )
        friend.users.remove(new_friend)

    def __str__(self):
        return str(self.current_user)

# class FriendRequest(models.Model):
#     authorID = models.CharField(max_length=40, unique=True)
#     type = models.CharField(max_length=100, default="text/plain")
#     summary = models.CharField(max_length=100, default="text/plain")
#     new_follower_ID = models.CharField(max_length=40, primary_key=True)
#
#     def get_author(self):
#         return self.authorID
#
#     def get_type(self):
#         return "Follow"
#
#     def get_actor(self):
#         return self.new_follower_ID

class Comment(models.Model):
    # model_type = models.CharField(max_length=10, default= "comment")
    comment = models.TextField()
    contentType = models.CharField(max_length=20, default="text/plain")
    published = models.DateTimeField(auto_now_add=True)
    commentID = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True)
    author_write_comment_ID = models.CharField(max_length=40)
    author_write_article_ID = models.CharField(max_length=40)
    postID = models.ForeignKey(Post, on_delete=models.CASCADE)
    # def get_id(self):
    # return settings.HOST_URL + "author/" + self.authorID

    def get_comment_id(self):
        return "{}author/{}/posts/{}/comments/{}".format(settings.HOST_URL, self.author_write_article_ID, str(self.postID.postID),str(self.commentID))

    def get_type(self):
        return "comment"

class Inbox(models.Model):
    authorID = models.CharField(max_length=40, unique=True)
    items = ArrayField(models.JSONField(), default=list) # array of objects

    def get_author(self):
        return settings.HOST_URL + "author/" + self.authorID

    def get_type(self):
        return "inbox"

class LikePost(models.Model):
    type = models.CharField(max_length=100)
    at_context = models.URLField(max_length=200)
    summary = models.CharField(max_length=100)
    published = models.DateTimeField(auto_now_add=True)
    likeID = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True)
    author_like_ID = models.CharField(max_length=40)
    author_write_article_ID = models.CharField(max_length=40)
    postID = models.ForeignKey(Post, on_delete=models.CASCADE)

    def get_like_model(self):
        return "{}author/{}/posts/{}".format(settings.HOST_URL, self.author_write_article_ID, str(self.postID.postID))


class LikeComment(models.Model):
    type = models.CharField(max_length=100)
    at_context = models.URLField(max_length=200)
    summary = models.CharField(max_length=100)
    published = models.DateTimeField(auto_now_add=True)
    likeID = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True)
    author_like_ID = models.CharField(max_length=40)
    author_write_article_ID = models.CharField(max_length=40)
    postID = models.ForeignKey(Post, on_delete=models.CASCADE)
    commentID = models.ForeignKey(Comment, on_delete=models.CASCADE)

    def get_like_model(self):
        return "{}author/{}/posts/{}/comments/{}".format(settings.HOST_URL, self.author_write_article_ID, str(self.postID.postID),str(self.commentID.commentID))

class Liked(models.Model):
    authorID = models.CharField(max_length=40, unique=True)
    items = ArrayField(models.JSONField(), default=list) # array of objects

    def get_type(self):
        return "liked"
