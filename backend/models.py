import uuid
from typing import Union
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from rest_framework.request import Request

from social_dist.settings import DJANGO_DEFAULT_HOST 

class Author(models.Model):
    # This is the UUID for the author
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # one2one relation with django user
    user = models.OneToOneField(User, on_delete=models.CASCADE) 
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
        ("FOLLOWERS", "FOLLOWERS"),
        ("PRIVATE", "PRIVATE")
    ]
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
    # When the post was published
    published = models.DateTimeField('date published', auto_now_add=True)
    # What is the visibility level of the Post
    visibility = models.CharField(max_length=30, choices = VISIBILITY, default="PUBLIC")

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
    def _get_absolute_url(self) -> str:
        """
        This will return the absolute url for this post

        args: None

        return: The url of the post
        """
        url = reverse('post-detail', args=[str(self.author.id),str(self.id)])
        url = url.replace("api/","")
        return url

    def update_url_field(self):
        """
        This will update the url field of the post based on the object's author url (homepage) and post's id

        args:
            - request : The request that contains the url to update from

        return: None
        """
        self.url = str(self.author.url) + 'posts/' + str(self.id)
        self.save()

    
class Comment(models.Model):
    CONTENT_TYPES = [
        ("text/markdown", "text/markdown"),
        ("text/plain", "text/plain"),
        ("application/base64","application/base64"),
        ("image/png;base64","image/png;base64"),
        ("image/jpeg;base64","image/jpeg;base64")
    ]
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

    def _get_absolute_url(self) -> str:
        """
        This will return the absolute url for this comment

        args: None

        return: The url of the comment
        """
        url = reverse('comment-detail', args=[str(self.author.id),str(self.post.id),str(self.id)])
        url = url.replace("api/", "")
        return url

    def update_url_field_with_request(self, request):
        """
        This will update the url fields of the comment based on the url of the current request

        args:
            - request : The request that contains the url to update from
            
        return: None
        """
        self.url = request.build_absolute_uri(self._get_absolute_url())
        self.save()

#for likes on a post
class PostLike(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    #not sure what to do for @context
    post = models.ForeignKey(Post, related_name='likes',on_delete = models.CASCADE)
    author = models.ForeignKey(Author, related_name='posts_liked',on_delete = models.CASCADE)
    summary = models.CharField(max_length=200)
    class Meta:
        unique_together = (("author","post"))
    def get_object(self) ->  str:
        """
        This will return the url of the object being liked.

        args: None

        return: The url of the post
        """
        post_url = self.post._get_absolute_url()
        return post_url
    
        
class CommentLike(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    #not sure what to do for @context
    comment = models.ForeignKey(Comment, related_name='likes',on_delete = models.CASCADE)
    author = models.ForeignKey(Author,related_name='comments_liked',on_delete = models.CASCADE)
    summary = models.CharField(max_length=200)
    class Meta:
        unique_together = (("author","comment"))
    def get_object(self) ->  str:
        """
        This will return the url of the object being liked.

        args: None

        return: The url of the comment
        """
        comment_url = self.comment._get_absolute_url()
        return comment_url

class Like(models.Model):
    #not sure what to do for @context
    object = models.URLField(max_length=500, editable=False)
    author = models.ForeignKey(Author,on_delete = models.CASCADE)
    type = models.CharField(default = "Like",max_length=200)
    summary = models.CharField(max_length=200)

#The inbox of the user not needed but kept for now in case we change our minds
#class Inbox(models.Model):
#    author = models.ForeignKey(Author, on_delete = models.CASCADE)

class FriendRequest(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    #summary of the friend request
    summary = models.CharField(max_length=200)
    #the author who is making the friend request
    requestor = models.ForeignKey(Author, related_name='sent_friend_requests', on_delete = models.CASCADE)
    #the author who is being asked if they want to be friends
    requestee = models.ForeignKey(Author, related_name='friend_requests', on_delete = models.CASCADE)
    class Meta:
        unique_together = (("requestor","requestee"))

class InboxPost(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    #This is the post sent to the inbox
    post = models.ForeignKey(Post, related_name='sent_to', on_delete = models.CASCADE)
    #This is the author whose inbox it is sent to
    author = models.ForeignKey(Author, related_name='posts_in_inbox', on_delete = models.CASCADE)
    class Meta:
        unique_together = (("author","post"))

class InboxComment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    #This is the comment sent to the inbox
    comment = models.ForeignKey(Comment, on_delete = models.CASCADE)
    #This is the author whose inbox it is sent to
    author = models.ForeignKey(Author, related_name='comments_in_inbox', on_delete = models.CASCADE)
    class Meta:
        unique_together = (("author","comment"))

class InboxPostLike(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    #This is the post like sent to the inbox
    post_like = models.OneToOneField(PostLike, related_name='sent_to', on_delete = models.CASCADE)
    #This is the author whose inbox it is sent to
    author = models.ForeignKey(Author, related_name='post_likes_in_inbox', on_delete = models.CASCADE)
    class Meta:
        unique_together = (("author","post_like"))
    
class InboxCommentLike(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    #This is the comment like sent to the inbox
    comment_like = models.OneToOneField(CommentLike, related_name='sent_to', on_delete = models.CASCADE)
    #This is the author whose inbox it is sent to
    author = models.ForeignKey(Author, related_name='comment_likes_in_inbox', on_delete = models.CASCADE)
    class Meta:
        unique_together = (("author","comment_like"))

class InboxFriendRequest(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    #This is the friend request sent to the inbox
    friend_request = models.OneToOneField(FriendRequest, related_name='sent_to', on_delete = models.CASCADE)
    #This is the author whose inbox it is sent to
    author = models.ForeignKey(Author, related_name='friend_requests_in_inbox', on_delete = models.CASCADE)
    class Meta:
        unique_together = (("author","friend_request"))

