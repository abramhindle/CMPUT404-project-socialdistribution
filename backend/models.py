# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from django.contrib.postgres.fields import ArrayField

import uuid


class Host(models.Model):
    url = models.URLField(max_length=400)
    serviceAccountUsername = models.CharField(
        max_length=100, null=True, blank=True)
    serviceAccountPassword = models.CharField(
        max_length=100, null=True, blank=True)


class User(AbstractUser):
    githubUrl = models.URLField(max_length=400, blank=True)
    host = models.ForeignKey(
        Host, null=True, blank=True, on_delete=models.CASCADE)

    def get_full_user_id(self):
        user_host = self.host.url
        if user_host[-1] == "/":
            user_host = user_host[:-1]

        return "{}/author/{}".format(user_host, self.id)

    def get_friends(self):
        friend_ids = Friend.objects.filter(
            fromUser_id=self.id).values_list('toUser_id', flat=True)
        friend_list = User.objects.filter(id__in=friend_ids)

        return friend_list

    def get_fof(self):
        fof = User.objects.none()
        friends = self.get_friends()

        for friend in friends:
            friend_ids = friend.get_friends().exclude(id=self.id)
            fof |= User.objects.filter(id__in=friend_ids)

        return fof.distinct()


class Post(models.Model):
    VISIBILITY_CHOICES = (
        ("PUBLIC", "PUBLIC"),
        ("FOAF", "FOAF"),
        ("FRIENDS", "FRIENDS"),
        ("PRIVATE", "PRIVATE"),
        ("SERVERONLY", "SERVERONLY"),
        ("UNLISTED", "UNLISTED"),
    )

    postId = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    timestamp = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
    # Visibility can be one of the followings : "PUBLIC","PRIVATE","Private","FRIENDS","FOF" or specific user ID
    visibility = models.CharField(
        max_length=10, choices=VISIBILITY_CHOICES, default="PUBLIC")
    visibleTo = ArrayField(models.CharField(
        max_length=200), blank=True, default=list)

    def is_unlisted(self):
        if self.visibility == "UNLISTED":
            return True
        else:
            return False

    def get_visible_users(self):
        if self.visibility == "PUBLIC":
            users = User.objects.all()
        elif self.visibility == "FRIENDS":
            users = self.author.get_friends()
        elif self.visibility == "FOAF":
            users = self.author.get_friends()
            users |= self.author.get_fof()
        elif self.visibility == "PRIVATE":
            users = User.objects.none()
            visible_to = self.visibleTo

            for user in User.objects.all():
                if user.get_full_user_id() in visible_to:
                    users |= User.objects.filter(host=user.host, id=user.id)

        elif self.visibility == "UNLISTED":
            users = User.objects.none()
        # TODO add serveronly

        return users.distinct()


class Comments(models.Model):
    commentId = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    content = models.TextField()
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    postedBy = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="comment_postedBy")
    postedTo = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="comment_postedTo")


class FriendRequest(models.Model):
    fromUser = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="friendRequest_fromUser")
    toUser = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="friendRequest_toUser")
    isAccepted = models.BooleanField(default=False)
    sentDate = models.DateTimeField(auto_now_add=True)


class Friend(models.Model):
    fromUser = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="friend_fromUser")
    toUser = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="friend_toUser")
    friendDate = models.DateTimeField(auto_now_add=True)
    unfriendDate = models.DateTimeField(null=True, blank=True)
