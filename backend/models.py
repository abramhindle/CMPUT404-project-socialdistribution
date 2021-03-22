from django.db import models
from django.contrib.auth.models import User
from django.db.models.fields import related
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
import uuid

def generate_uuid():
	return uuid.uuid4().hex

class Author(models.Model):
	id = models.CharField(primary_key=True, default=generate_uuid, max_length=100, unique=True, editable=False)
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True, editable=False)
	token = models.CharField(default="1234", max_length=100)
	displayName = models.CharField(max_length=100, unique=True)
	github = models.URLField()
	host = models.URLField()
	url = models.URLField()

class Post(models.Model):
	id = models.CharField(primary_key=True, default=generate_uuid, unique=True, max_length=100)
	author = models.ForeignKey(Author, on_delete=models.CASCADE)
	title = models.CharField(max_length=100)
	source = models.URLField()
	origin = models.URLField()
	description = models.CharField(max_length=100)
	content_type = models.CharField(max_length=50)
	content = models.CharField(max_length=500, null=True, blank=True)
	# image_content = models.ImageField(upload_to="backend/media/post/", null=True, blank=True) # TODO: Make sure we can use images like this
	image_content = models.TextField(null=True, blank=True)
	categories = models.JSONField() # TODO: Maybe make a seperate table to store multiple categories for querying
	# count = models.PositiveIntegerField(default=0)
	published = models.DateTimeField(auto_now_add=True)
	visibility = models.CharField(max_length=20)
	unlisted = models.BooleanField(default=False)
	host = models.CharField(max_length=50)

class Comment(models.Model):
	id = models.CharField(primary_key=True, default=generate_uuid, editable=False, unique=True, max_length=100)
	post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
	author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='author')
	comment = models.CharField(max_length=500, null=True)
	image_content = models.ImageField(null=True, upload_to="backend/media/comment/", blank=True)
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
