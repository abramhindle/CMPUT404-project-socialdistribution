from django.db import models
import uuid
from django.contrib.auth.models import AbstractUser
from preferences.models import Preferences
import requests
import json
from urllib.parse import urlparse
from requests.auth import HTTPBasicAuth
from django.contrib.sites.models import Site
from django.urls import reverse
from dispersal.settings import SITE_URL


# Create your models here.


class WWUser(models.Model):
    url = models.URLField(blank=False, unique=True)
    local = models.BooleanField(default=False)
    user_id = models.UUIDField(null=True, unique=True)

    def __str__(self):
        return str(self.user_id)

class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    displayName = models.CharField(max_length=200)
    github = models.URLField(blank=True)
    bio = models.CharField(max_length=256, blank=True)
    approved = models.BooleanField(default=False)
    githubLastId = models.CharField(max_length=64, blank=True)
    host = models.CharField(default=SITE_URL, max_length=400)


    def is_approved(self):
        return self.approved


class Follow(models.Model):
    # The one who is being followed
    followee = models.ForeignKey(WWUser, to_field='url', related_name='followee', on_delete=models.CASCADE)
    # The one who is following
    follower = models.ForeignKey(WWUser, related_name='follower', to_field='url', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('follower', 'followee')

    def __str__(self):
        return str(self.follower) + " is following " + str(self.followee)


class FollowRequest(models.Model):
    # The user being requested to follow the requester back. The target of the request
    requestee = models.ForeignKey(WWUser, to_field='url', related_name='requestee', on_delete=models.CASCADE)
    # The user requesting to be followed back
    requester = models.ForeignKey(WWUser, to_field='url', related_name='requester', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('requester', 'requestee')

    def __str__(self):
        return str(self.requester) + " requested that " + str(self.requestee) + " become their friend/follower"


class Server(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    server = models.URLField(max_length=200, unique=True)
    username = models.CharField(max_length=200, null=True)
    password = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.server

    def get_author_info(self, author_id):
        username = self.username
        password = self.password
        url = self.server + '/author/{}'.format(author_id)
        try:
            r = requests.get(url, auth=HTTPBasicAuth(username, password))
            if r.status_code == 200:
                user_data = r.content.decode('utf-8')
                user_data = json.loads(user_data)
                user_data['id'] = self.__parse_id_from_url(user_data['id'])
                user_data['host'] = self.server
                user = UserSerializer(data=user_data)
                WWUser.objects.get_or_create(url=url, user_id=user_data['id'])
                return user.to_user_model()
        except Exception as e:
            pass
        return None

    def get_author_posts(self, author_id, requestor):
        url = self.server + '/author/{AUTHOR_ID}/posts/'.format(AUTHOR_ID=author_id)
        headers = {'X-Request-User-ID': 'http://{}{}'.format((Site.objects.get_current().domain),
                                                        reverse('author', kwargs={'pk': requestor}))}
        try:
            r = requests.get(url, auth=HTTPBasicAuth(self.username, self.password), headers=headers)

            if r.status_code == 200:
                posts_data = r.content.decode('utf-8')
                posts_data = json.loads(posts_data)
                if (len(posts_data['posts']) == 0):
                    return None
                return posts_data['posts']
        except:
            pass
        return None

    def get_external_post(self, post_id, requestor):
        url = self.server + '/posts/{}'.format(post_id)
        requestor_serialized = UserSerializer(instance=requestor)
        ww_requestor = get_ww_user(requestor.id)
        requestor_friends = get_friends(ww_requestor)
        headers = {'X-Request-User-ID': 'https://{}{}'.format((Site.objects.get_current().domain),
                                                              reverse('author', kwargs={'pk': requestor})),
                   }
        post_data = {
            "query": "getpost",
            'postid': post_id,
            'url': url,
            'author': requestor_serialized.data,
            'friends': [x for x in requestor_friends]
        }

        try:

            r = requests.post(url, json=post_data, auth=HTTPBasicAuth(self.username, self.password), headers=headers)

            if r.status_code == 200:
                posts_data = r.content.decode('utf-8')
                posts_data = json.loads(posts_data)
                return posts_data[0]
            # IF people don't follow spec, try a GET
            if r.status_code == 405 or r.status_code == 400:
                r2 = requests.get(url, auth=HTTPBasicAuth(self.username, self.password), headers=headers)
                if r2.status_code == 200:
                    posts_data = r2.content.decode('utf-8')
                    posts_data = json.loads(posts_data)
                    return posts_data['posts'][0]
        except Exception as e:
            pass
        return None

    def send_external_friendrequest(self, requestee, requestor):
        url = self.server + '/friendrequest'
        headers = {'X-Request-User-ID': '{}'.format(requestor['id']),
                   }

        post_data = {
            "query": "friendrequest",
            'author': requestor,
            'friend': requestee
        }

        try:

            r = requests.post(url, json=post_data, auth=HTTPBasicAuth(self.username, self.password), headers=headers)

            if r.status_code == 200:
                posts_data = r.content.decode('utf-8')
                posts_data = json.loads(posts_data)
                return posts_data
        except:
            pass
        return None

    def __parse_id_from_url(self, url):
        """
        Parses a user id from user urls in the form:
        https://example.com/author/f3be7f78-d878-46c5-8513-e9ef346a759d/
        """
        parsed = urlparse(url)
        path = parsed.path.strip('/')
        path = path.split('/')
        return path[-1]

class Category(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    category = models.CharField(max_length=30, blank=True)

    def __str__(self):
        return self.category


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

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200)
    source = models.URLField(blank=True)
    origin = models.URLField(blank=True)
    description = models.CharField(max_length=400)
    contentType = models.CharField(max_length=18, choices=CONTENTCHOICES, default="text/plain")
    content = models.TextField()
    published = models.DateTimeField(auto_now_add=True)
    visibility = models.CharField(max_length=7, choices=VISIBILITY, default="PUBLIC")
    unlisted = models.BooleanField(default=False)
    # visibleTo = models.ForeignKey(ExternalUser, related_name='visible_posts', on_delete=models.DO_NOTHING, null=True)
    author = models.ForeignKey(User, related_name='posts', on_delete=models.CASCADE)
    categories = models.ManyToManyField(Category, blank=True)


class Viewer(models.Model):
    # id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    url = models.URLField()
    post = models.ForeignKey(Post, related_name="visibleTo", on_delete=models.CASCADE)

    def __str__(self):
        return self.url


class Comment(models.Model):
    PLAIN = "text/plain"
    CONTENTCHOICES = (
        ("text/plain", "Plain"),
        ("text/markdown", "Markdown")
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    parent_post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    author = models.ForeignKey(WWUser, to_field='url', related_name='comments', on_delete=models.CASCADE)
    comment = models.CharField(max_length=1024)
    contentType = models.CharField(max_length=18, choices=CONTENTCHOICES, default=PLAIN)
    # ISO 8601 TIMESTAMP
    published = models.DateTimeField(auto_now_add=True)


class SitePreferences(Preferences):
    serve_others_images = models.BooleanField(default=True)
    serve_others_posts = models.BooleanField(default=True)


from .serializers import UserSerializer
from .helpers import get_friends, get_ww_user, get_user
