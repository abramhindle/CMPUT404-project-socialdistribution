from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
import uuid
from .utils import join_urls
from .converters import Converter, Team10Converter, Team11Converter
from urllib.parse import urlparse
from .api_client import http_request, async_http_request
import concurrent.futures
import logging
from django.http.request import HttpRequest
from django.urls import reverse

logger = logging.getLogger(__name__)

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
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
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
    
    # dynamically determines the author's full url
    # e.g. http://socialdistribution.com/api/authors/1234/
    def get_url(self, request: HttpRequest):
        return request.build_absolute_uri(reverse('author-detail', args=(self.id,)))


class NodeManager(models.Manager):
    # raises Node.DoesNotExist if no matching node is found
    def get_node_with_url(self, url):
        hostname = urlparse(url).hostname
        return self.get_queryset().get(api_url__contains=hostname)


class Node(models.Model):
    user = models.OneToOneField(Author, on_delete=models.CASCADE)
    api_url = models.URLField(max_length=300, unique=True)
    auth_username = models.CharField(max_length=300)
    auth_password = models.CharField(max_length=300)
    objects = NodeManager()
    # each new team will need to have a new converter
    TEAM_CHOICES = [
        (10, 10),
        (11, 11),
        (14, 14),
    ]
    team = models.IntegerField(choices=TEAM_CHOICES, default=14)
    
    def get_converter(self):
        if self.team == 14:
            return Converter()
        elif self.team == 11:
            return Team11Converter()
        elif self.team == 10:
            return Team10Converter()
        raise Exception("No converter for team {}".format(self.team))
    
    def get_authors_url(self):
        # assumes that /authors route applies to all nodes
        return join_urls(self.api_url, "authors")


class RemoteAuthorManager(models.Manager):
    # returns a RemoteAuthor object if it exists, otherwise None
    def attempt_find(self, author_id):
        try:
            author = self.get_queryset().get(id=author_id)
            return author
        except RemoteAuthor.DoesNotExist:
            for node in Node.objects.all():
                url = join_urls(node.get_authors_url(), author_id)
                res, _ = http_request("GET", url=url, node=node, expected_status=200)
                if res is not None:
                    author = node.get_converter().convert_author(res)
                    # cache the author id to save some network requests the next time
                    author = RemoteAuthor.objects.create(id=author["id"], node=node)
                    return author
        return None
    

class RemoteAuthor(models.Model):
    id = models.UUIDField(primary_key=True)
    node = models.ForeignKey(Node, on_delete=models.CASCADE)
    objects = RemoteAuthorManager()

    def get_absolute_url(self):
        return join_urls(self.node.api_url, "authors", str(self.id))
    
    def get_inbox_url(self):
        return join_urls(self.get_absolute_url(), "inbox", ends_with_slash=True)


class RemotePost(models.Model):
    id = models.UUIDField(primary_key=True)
    author = models.ForeignKey(RemoteAuthor, on_delete=models.CASCADE)
    
    def get_absolute_url(self):
        return join_urls(self.author.get_absolute_url(), "posts", str(self.id))


class FollowRequest(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    sender =  models.ForeignKey(Author, related_name='follow_requests_sent', on_delete=models.CASCADE, null=True)
    receiver =  models.ForeignKey(Author, related_name='follow_requests_received', on_delete=models.CASCADE)
    remote_sender = models.ForeignKey(RemoteAuthor, on_delete=models.CASCADE, null=True)
    
    class Meta:
        unique_together = [['sender', 'receiver'], ['remote_sender', 'receiver']]

class Follow(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    follower = models.ForeignKey(Author, related_name='following_authors', on_delete=models.CASCADE, null=True)
    followee = models.ForeignKey(Author, related_name='followed_by_authors', on_delete=models.CASCADE)
    remote_follower = models.ForeignKey(RemoteAuthor, on_delete=models.CASCADE, null=True)
    
    class Meta:
        unique_together = [['follower', 'followee'], ['remote_follower', 'followee']]

class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
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

    # TODO: how much work will it take to make all of the following POST requests async?
    # TODO: might need to add some retry logic for inbox updates over http
    
    def update_author_inbox_over_http(self, url, node, request):
        node_converter = node.get_converter()
        return http_request("POST", url=url, node=node, 
                            expected_status=node_converter.expected_status_code("send_post_inbox"),
                            json=node_converter.send_post_inbox(self, request), timeout=3)

    # returns True only if all requests were successful
    def send_to_followers(self, request):
        success = True
        followers = self.author.followed_by_authors.all()
        max_threads = min(10, len(followers))       # spawn at most 10 threads
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_threads) as executor:
            future_to_url = {}
            for follow in followers:
                if follow.remote_follower:
                    node = follow.remote_follower.node
                    url = follow.remote_follower.get_inbox_url()
                    future_to_url[executor.submit(
                        self.update_author_inbox_over_http, 
                        url=url,
                        node=node,
                        request=request
                    )] = url
                else:
                    Inbox.objects.create(target_author=follow.follower, post=self)
            for future in concurrent.futures.as_completed(future_to_url):
                url = future_to_url[future]
                try:
                    res, _ = future.result()
                    if res is None:
                        success = False
                except Exception as exc:
                    logger.error('%r generated an exception: %s' % (url, exc))
                    success = False
        return success
    
    # returns True only if all requests were successful
    def send_to_all_authors(self, request):
        success = True
        for author in Author.objects.exclude(id=self.author.id).iterator():
            Inbox.objects.create(target_author=author, post=self)
        # fetch all authors on all nodes and update their inboxes
        for node in Node.objects.all():
            node_converter = node.get_converter()
            res, _ = http_request("GET", node.get_authors_url(), node=node)
            if res is None:
                success = False
                continue
            authors = node_converter.convert_authors(res)
            max_threads = min(10, len(authors))       # spawn at most 10 threads
            with concurrent.futures.ThreadPoolExecutor(max_workers=max_threads) as executor:
                future_to_url = {}
                for author in authors:
                    url = join_urls(author["url"], "inbox", ends_with_slash=True)
                    future_to_url[executor.submit(
                        self.update_author_inbox_over_http,
                        url=url, node=node, request=request
                    )] = url

                for future in concurrent.futures.as_completed(future_to_url):
                    url = future_to_url[future]
                    try:
                        res, _ = future.result()
                        if res is None:
                            success = False
                    except Exception as exc:
                        logger.error('%r generated an exception: %s' % (url, exc))
                        success = False
        return success
    
    def get_url(self, request):
        return join_urls(self.author.get_url(request), "posts", str(self.id), ends_with_slash=True)


class Comment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
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
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    author = models.ForeignKey(Author,on_delete=models.CASCADE)
    post = models.ForeignKey(Post,on_delete=models.CASCADE,null=True)
    comment = models.ForeignKey(Comment,on_delete=models.CASCADE,null=True)

class Inbox(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    target_author = models.ForeignKey(Author,related_name='inbox',on_delete=models.CASCADE)
    follow_request_received = models.ForeignKey(FollowRequest, on_delete=models.CASCADE, null=True)
    post = models.ForeignKey(Post,on_delete=models.CASCADE,null=True)
    comment = models.ForeignKey(Comment,on_delete=models.CASCADE,null=True)
    like = models.ForeignKey(Like,on_delete=models.CASCADE,null=True)
    created_at = models.DateTimeField(verbose_name="date created",auto_now_add=True)
    remote_post = models.ForeignKey(RemotePost, on_delete=models.CASCADE, null=True)
