from email.policy import default
from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)

class AuthorUserManager(BaseUserManager):
    def create_user(self, username, password=None):
        """
        Creates and saves a User with the given username and password.
        """
        if not username:
            raise ValueError('Users must have a username')

        user = self.model(
            username=username,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None):
        """
        Creates and saves a superuser with the given username and password.
        """
        user = self.create_user(
            username,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class Author(AbstractBaseUser):
    username = models.CharField(max_length=300, unique=True)
    display_name = models.CharField(max_length=200)
    profile_image = models.CharField(max_length=250, blank=True)
    github_handle = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(verbose_name="date created", auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_remote_user = models.BooleanField(default=False)

    objects = AuthorUserManager()
    
    USERNAME_FIELD = 'username'

    def __str__(self):
        return self.display_name
    
    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin


class FollowRequest(models.Model):
    sender =  models.ForeignKey(Author, related_name='follow_requests_sent', on_delete=models.CASCADE)
    receiver =  models.ForeignKey(Author, related_name='follow_requests_received', on_delete=models.CASCADE)
    
    class Meta:
        unique_together = ['sender', 'receiver']

class Follow(models.Model):
    follower = models.ForeignKey(Author, related_name='following_authors', on_delete=models.CASCADE)
    followee = models.ForeignKey(Author, related_name='followed_by_authors', on_delete=models.CASCADE)
    
    class Meta:
        unique_together = ['follower', 'followee']

class Post(models.Model):

    author = models.ForeignKey(Author,on_delete=models.CASCADE)
    created_at = models.DateTimeField(verbose_name="date created",auto_now_add=True)
    edited_at = models.DateTimeField("date edited",null=True)
    title = models.CharField(max_length=300)
    description = models.TextField(blank=True)
    source = models.CharField(max_length=200,default='')
    origin = models.CharField(max_length=200,default='')
    unlisted = models.BooleanField(default=False) 

    VISIBILITY_CHOICES = [
        ("PUBLIC","Public"),
        ("FRIENDS","Friends"),
        ("PRIVATE","Private")
    ]
    visibility = models.CharField(max_length=200,choices=VISIBILITY_CHOICES,default="PUBLIC")
    CONTENT_TYPE_CHOICES = [
        ("text/plain","Plain text"),
        ("text/markdown","Markdown text")
    ]
    content_type = models.CharField(max_length=200,choices=CONTENT_TYPE_CHOICES,default="text/plain")
    content = models.TextField(blank=True)

class Comment(models.Model):
    author = models.ForeignKey(Author,on_delete=models.CASCADE)
    post = models.ForeignKey(Post,on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    CONTENT_TYPE_CHOICES = [
        ("text/plain","Plain text"),
        ("text/markdown","Markdown text")
    ]
    content_type = models.CharField(max_length=200,choices=CONTENT_TYPE_CHOICES,default="text/plain")


class Like(models.Model):
    author = models.ForeignKey(Author,on_delete=models.CASCADE)
    post = models.ForeignKey(Post,on_delete=models.CASCADE,null=True)
    comment = models.ForeignKey(Comment,on_delete=models.CASCADE,null=True)

class Inbox(models.Model):
    target_author = models.ForeignKey(Author,related_name='inbox',on_delete=models.CASCADE)
    follow_request_received = models.ForeignKey(FollowRequest, on_delete=models.CASCADE, null=True)
    post = models.ForeignKey(Post,on_delete=models.CASCADE,null=True)
    comment = models.ForeignKey(Comment,on_delete=models.CASCADE,null=True)
    like = models.ForeignKey(Like,on_delete=models.CASCADE,null=True)
    created_at = models.DateTimeField(verbose_name="date created",auto_now_add=True)


class Node(models.Model):
    user = models.OneToOneField(Author, on_delete=models.CASCADE)
    api_url = models.URLField(max_length=300, unique=True)
    # TODD: add fields that let us connect to remote nodes based on other groups' authentication schemes
