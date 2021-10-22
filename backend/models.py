import uuid
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

#Author class
class Author(models.Model):
    # This is the UUID for the author
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # one2one relation with django user
    user = models.OneToOneField(User, on_delete=models.CASCADE) 
    # The followers of this author, not a bidirectional relationship 
    followers = models.ManyToManyField('self', related_name='follower', blank=True, symmetrical=False)
    # The URL for the home host of the author
    host = models.URLField(editable=False)
    # The URL for the author's profile
    url = models.URLField(editable=False)
    # The display name of the author
    display_name = models.CharField(max_length=200, blank=True)
    # HATEOAS url for github API
    github_url = models.URLField(max_length=200, blank=True)

    def _get_absolute_url(self):
        return reverse('author-detail', args=[str(self.id)])
    
    def update_url_fields_with_request(self, request):
        self.url = request.build_absolute_uri(self._get_absolute_url())
        self.host = request.build_absolute_uri('/')
        self.save()

    def get_id(self):
        return self.url or self.id
    
    def __str__(self):
        return self.display_name +'-' + str(self.id)

# Post class
class Post(models.Model):
    #https://www.geeksforgeeks.org/how-to-use-django-field-choices/ for choices
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
    contentType = models.CharField(max_length=30, choices = CONTENT_TYPES, default="text/plain")
    # The main content of the post
    content = models.TextField(blank=True)

    author = models.ForeignKey(Author, on_delete = models.CASCADE, related_name='posted')

    #not sure what to do for category

    #should probably be a different field type
    published = models.DateTimeField('date published', auto_now_add=True)
    visibility = models.CharField(max_length=30, choices = VISIBILITY, default="PUBLIC")

    #https://www.geeksforgeeks.org/booleanfield-django-models/ for boolean fields
    unlisted = models.BooleanField(default=False)

    def __str__(self):
        return self.title + " (" + str(self.id) + ")"
    
    def get_id(self):
        return self.url or self.id
    
class Comment(models.Model):
    CONTENT_TYPES = [
        ("text/markdown", "text/markdown"),
        ("text/plain", "text/plain"),
        ("application/base64","application/base64"),
        ("image/png;base64","image/png;base64"),
        ("image/jpeg;base64","image/jpeg;base64")
    ]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    url = models.URLField(max_length=500, editable=False)
    post = models.ForeignKey(Post, on_delete = models.CASCADE, related_name='comments')
    author = models.ForeignKey(Author, on_delete = models.CASCADE)
    contentType = models.CharField(max_length=30,choices = CONTENT_TYPES, default= "text/plain")
    comment = models.TextField()
    #should probably be a different field type
    published = models.DateTimeField('date published', auto_now_add=True)

#for likes on a post
class PostLike(models.Model):
    #not sure what to do for @context
    post = models.ForeignKey(Post, on_delete = models.CASCADE)
    author = models.ForeignKey(Author, on_delete = models.CASCADE)
    summary = models.CharField(max_length=200)
    class Meta:
        unique_together = (("author","post"))
        
class CommentLike(models.Model):
    #not sure what to do for @context
    comment = models.ForeignKey(Comment, on_delete = models.CASCADE)
    author = models.ForeignKey(Author, on_delete = models.CASCADE)
    summary = models.CharField(max_length=200)
    class Meta:
        unique_together = (("author","comment"))

#The inbox of the user
#class Inbox(models.Model):
#    author = models.ForeignKey(Author, on_delete = models.CASCADE)

class FriendRequest(models.Model):
    #summary of the friend request
    summary = models.CharField(max_length=200)
    #the author who is making the friend request
    requestor = models.ForeignKey(Author, related_name='sent_friend_requests', on_delete = models.CASCADE)
    #the author who is being asked if they want to be friends
    requestee = models.ForeignKey(Author, related_name='friend_requests', on_delete = models.CASCADE)
    class Meta:
        unique_together = (("requestor","requestee"))

class InboxPost(models.Model):
    #This is the post sent to the inbox
    post = models.ForeignKey(Post, related_name='sent_to', on_delete = models.CASCADE)
    #This is the author whose inbox it is sent to
    author = models.ForeignKey(Author, related_name='posts_in_inbox', on_delete = models.CASCADE)
    class Meta:
        unique_together = (("author","post"))

class InboxPostLike(models.Model):
    #This is the post like sent to the inbox
    post_like = models.ForeignKey(PostLike, related_name='sent_to', on_delete = models.CASCADE)
    #This is the author whose inbox it is sent to
    author = models.ForeignKey(Author, related_name='post_likes_in_inbox', on_delete = models.CASCADE)
    class Meta:
        unique_together = (("author","post_like"))
    
class InboxCommentLike(models.Model):
    #This is the comment like sent to the inbox
    comment_like = models.ForeignKey(CommentLike, related_name='sent_to', on_delete = models.CASCADE)
    #This is the author whose inbox it is sent to
    author = models.ForeignKey(Author, related_name='comment_likes_in_inbox', on_delete = models.CASCADE)
    class Meta:
        unique_together = (("author","comment_like"))

class InboxFriendRequest(models.Model):
    #This is the friend request sent to the inbox
    friend_request = models.ForeignKey(FriendRequest, related_name='sent_to', on_delete = models.CASCADE)
    #This is the author whose inbox it is sent to
    author = models.ForeignKey(Author, related_name='friend_requests_in_inbox', on_delete = models.CASCADE)
    class Meta:
        unique_together = (("author","friend_request"))

