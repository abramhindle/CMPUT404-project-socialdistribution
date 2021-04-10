from django.db import models
from django.contrib.auth.models import User
from django.db.models.fields import related
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
import uuid
from manager.settings import HOSTNAME

def generate_uuid():
	return uuid.uuid4().hex

class Node(models.Model):
	host = models.CharField(primary_key=True, default=HOSTNAME, max_length=200)
	user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)
	remote_username = models.CharField(max_length=150)
	remote_password = models.CharField(max_length=150)


class Author(models.Model):
	id = models.CharField(primary_key=True, default=generate_uuid, max_length=100, unique=True, editable=False)
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True, editable=False)
	token = models.CharField(default="1234", max_length=100)
	displayName = models.CharField(max_length=100)
	github = models.URLField(default=('https://github.com/'))
	host = models.CharField(default=HOSTNAME, max_length=200)
	url = models.URLField()

class Post(models.Model):
	id = models.CharField(primary_key=True, default=generate_uuid, unique=True, max_length=100)
	author = models.ForeignKey(Author, on_delete=models.CASCADE)
	title = models.CharField(max_length=100)
	source = models.URLField(default=HOSTNAME)
	origin = models.URLField(default=HOSTNAME)
	description = models.CharField(max_length=100)
	contentType = models.CharField(max_length=50)
	content = models.CharField(max_length=500, null=True, blank=True)
	image_content = models.TextField(null=True, blank=True)
	categories = models.JSONField()
	published = models.DateTimeField(auto_now_add=True)
	visibility = models.CharField(max_length=20)
	unlisted = models.BooleanField(default=False)
	host = models.CharField(max_length=50)

class Comment(models.Model):
	id = models.CharField(primary_key=True, default=generate_uuid, editable=False, unique=True, max_length=100)
	post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
	author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='author')
	comment = models.CharField(max_length=500, null=True)
	image_content = models.TextField(null=True, blank=True)
	published = models.DateTimeField(auto_now_add=True)
	contentType = models.CharField(max_length=50)
	host = models.CharField(max_length=50)
	post_author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='post_author')

class Like(models.Model):
	id = models.CharField(primary_key=True, default=generate_uuid, editable=False, unique=True, max_length=100)
	post = models.ForeignKey(Post, on_delete=models.CASCADE)
	author = models.ForeignKey(Author, on_delete=models.CASCADE)
	comment = models.ForeignKey(Comment, on_delete=models.CASCADE, null=True, blank=True)
	summary = models.CharField(max_length=100, default="Someone Likes your post")

class Follow(models.Model):
	id = models.CharField(primary_key=True, default=generate_uuid, editable=False, unique=True, max_length=100)
	follower = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='follower')
	followee = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='followee')
	friends = models.BooleanField(default=False)
	summary = models.CharField(max_length=200, default="Follow")

class Inbox(models.Model):
	id = models.CharField(primary_key=True, default=generate_uuid, editable=False, unique=True, max_length=100)
	author = models.ForeignKey(Author, on_delete=models.CASCADE)
	post = models.ForeignKey(Post, on_delete=models.CASCADE, blank=True, null=True,related_name='post')
	follow = models.ForeignKey(Follow, on_delete=models.CASCADE, blank=True, null=True, related_name='follow')
	like = models.ForeignKey(Like, on_delete=models.CASCADE, blank=True, null=True, related_name='like')
	icomment = models.ForeignKey(Comment, on_delete=models.CASCADE, blank=True, null=True, related_name='icomment')
