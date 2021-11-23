import uuid
from typing import Union
from django.db import models
from django.db.models import constraints
from django.urls import reverse
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from rest_framework.request import Request

from social_dist.settings import DJANGO_DEFAULT_HOST 

class Author(models.Model):
    # The type which should be constant
    type = models.CharField(max_length=6, default="author", editable=False)
    # This is the UUID for the author
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # one2one relation with django user
    # Also includes remote users as well
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True) 
    # The followers of this author, not a bidirectional relationship 
    followers = models.ManyToManyField('self', related_name='follower', blank=True, symmetrical=False)
    # The URL for the home host of the author
    host = models.URLField(editable=False, default=DJANGO_DEFAULT_HOST)
    # The URL for the author's profile
    url = models.URLField(editable=False)
    # The display name of the author
    display_name = models.CharField(max_length=200, blank=True)
    # HATEOAS url for github API
    github_url = models.URLField(max_length=200, blank=True)
    # Image profile
    profile_image = models.URLField(max_length=200, blank=True)
    
    def update_url_field(self):
        """
        This will update the url field of the author based on the id

        args:
            - request : The request that contains the url to update from

        return: None
        """
        self.url = str(self.host) + 'author/' + str(self.id)
        self.save()

    def get_id(self) -> Union[str, uuid.UUID]:
        """
        This will return the id of the author.
        If the url is not defined then the uuid will be return

        args: None

        return: The id of the author
        """
        return self.url or self.id
    
    def __str__(self) -> str:
        return self.display_name +'-' + str(self.id)

# https://simpleisbetterthancomplex.com/tutorial/2017/02/18/how-to-create-user-sign-up-view.html
@receiver(post_save, sender=User)
def update_profile_signal(sender, instance, created, **kwargs):
    if created:
        Author.objects.create(user=instance)
    instance.author.save()

# Post class
class Post(models.Model):
    # https://www.geeksforgeeks.org/how-to-use-django-field-choices/ for choices
    CONTENT_TYPES = [
        ("text/markdown", "text/markdown"),
        ("text/plain", "text/plain"),
        ("application/base64","application/base64"),
        ("image/png;base64","image/png;base64"),
        ("image/jpeg;base64","image/jpeg;base64")
    ]
    VISIBILITY = [
        ("PUBLIC", "PUBLIC"),
        ("FRIENDS", "FRIENDS"),
        ("PRIVATE", "PRIVATE")
    ]
    # The type which should be constant
    type = models.CharField(max_length=4, default="post", editable=False)
    # The UUID for the post
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # The URL for the post
    url = models.URLField(max_length=500, editable=False)
    # The title of the post
    title = models.CharField(max_length=200)
    # Where did you get this post from
    source = models.URLField(max_length=500, blank=True)
    # Where is it actually from
    origin = models.URLField(max_length=500, blank=True)
    # A tweet length description of the post
    description = models.CharField(max_length=240, blank=True)
    # The content type for the HTTP header
    content_type = models.CharField(max_length=30, choices = CONTENT_TYPES, default="text/plain")
    # The main content of the post
    content = models.TextField(blank=True)
    # The author object of who created the post
    author = models.ForeignKey(Author, on_delete = models.CASCADE, related_name='posted')
    # Categories is represented as a stringify JSON list 
    categories = models.TextField(default='[]')
    # When the post was published
    published = models.DateTimeField('date published', auto_now_add=True)
    # What is the visibility level of the Post
    visibility = models.CharField(max_length=30, choices = VISIBILITY, default="PUBLIC")
    # Where the comments for this post is located
    comment_url = models.URLField(max_length=500, editable=False, default=str(url) + '/comments')
    #https://www.geeksforgeeks.org/booleanfield-django-models/ for boolean fields
    unlisted = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.title + " (" + str(self.id) + ")"
    
    def get_id(self) ->  Union[str, uuid.UUID]:
        """
        This will return the id of the post.
        If the url is not defined then the uuid will be return

        args: None

        return: The id of the post
        """
        return self.url or self.id
    def get_num_likes(self):
        """
        This will return the number of likes for this post
        """
        return Like.objects.filter(object=self.url).count()

    def _get_absolute_url(self) -> str:
        """
        This will return the absolute url for this post

        args: None

        return: The url of the post
        """
        url = reverse('post-detail', args=[str(self.author.id),str(self.id)])
        # We want to remove the api prefix from the object
        url = url.replace("api/","")
        return url

    def update_url_field(self):
        """
        This will update the url field of the post based on the object's author url (homepage) and post's id

        args:
            - request : The request that contains the url to update from

        return: None
        """
        self.url = str(self.author.url) + '/posts/' + str(self.id)
        self.comment_url = str(self.author.host) + 'api/author/' + str(self.author.id) + '/posts/' + str(self.id) + '/comments'
        self.save()
    
    def get_comment_url(self):
        """
        This will return the comment URL for this post
        """
        return str(self.author.host) + 'api/author/' + str(self.author.id) + '/posts/' + str(self.id) + '/comments'

    
class Comment(models.Model):
    CONTENT_TYPES = [
        ("text/markdown", "text/markdown"),
        ("text/plain", "text/plain"),
        ("application/base64","application/base64"),
        ("image/png;base64","image/png;base64"),
        ("image/jpeg;base64","image/jpeg;base64")
    ]
    # The type which should be constant
    type = models.CharField(max_length=7, default="comment", editable=False)
    # The UUID of the comment
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # The URL of the comment
    url = models.URLField(max_length=500, editable=False)
    # The post object that the comment is associated with 
    post = models.ForeignKey(Post, on_delete = models.CASCADE, related_name='comments')
    # The author object of the comment
    author = models.ForeignKey(Author, on_delete = models.CASCADE)
    # The content type of the comment
    content_type = models.CharField(max_length=30,choices = CONTENT_TYPES, default= "text/plain")
    # The comment body
    comment = models.TextField()
    # The date when the comment was created
    published = models.DateTimeField('date published', auto_now_add=True)

    def get_id(self) -> Union[str, uuid.UUID]:
        """
        This will return the id of the comment.
        If the url is not defined then the uuid will be return

        args: None

        return: The id of the comment
        """
        return self.url or self.id

    def get_num_likes(self):
        """
        This will return the number of likes for this comment
        """
        return Like.objects.filter(object=self.url).count()

    def update_url_field(self):
        """
        This will update the url fields of the comment based on post's url 

        args:
            - request : The request that contains the url to update from
            
        return: None
        """
        self.url = str(self.post.url) + "/comments/" + str(self.id)
        self.save()

class Like(models.Model):
    # The type should be constant
    type = models.CharField(max_length=4, default="Like", editable=False)
    # The URL of the object being liked
    object = models.URLField(max_length=500, editable=False)
    # The author of the like
    author = models.ForeignKey(Author, related_name='liked',on_delete = models.CASCADE)
    summary = models.CharField(max_length=200)
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['author','object'], name="unique_like")
        ]

class FriendRequest(models.Model):
    # The type should be constant
    type = models.CharField(max_length=6, default="Follow", editable=False)
    # The id of the Friend Request
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # Summary of the friend request
    summary = models.CharField(max_length=200)
    # The author who is making the friend request
    actor = models.ForeignKey(Author, related_name='sent_friend_requests', on_delete = models.CASCADE, default="")
    # The recipient author of the Friend Request 
    object = models.ForeignKey(Author, related_name='recipient_friend_requests', on_delete = models.CASCADE, default="")
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['actor','object'], name="unique_friend_request")
        ]

# This is the inbox section
class Inbox(models.Model):
    # The type should be constant
    type = models.CharField(max_length=5, default="inbox", editable=False)
    # The id should be the author
    id = models.OneToOneField(Author, related_name="inbox", on_delete=models.CASCADE, primary_key=True)

    posts = models.ManyToManyField(Post, related_name="inbox_post", blank=True, symmetrical=False)
    likes = models.ManyToManyField(Like, related_name="inbox_like", blank=True, symmetrical=False)
    friend_requests = models.ManyToManyField(FriendRequest, related_name="inbox_friend_request", blank=True, symmetrical=False)

# This is the node section 
class Node(models.Model):
    host = models.URLField(primary_key=True)
    #basic auth info that must be provided by remote server when making requests to our server
    auth_info = models.CharField(max_length=100)

    #basic auth info that must be provided by our server when making requests to foreign servers
    #connecting_auth_info = models.CharField(max_length=100)

    def __str__(self):
        return str(self.host)
    def __auth__(self):
        return str(self.auth_info)

