import datetime
from django.db import models
from author.models import Author


# Create your models here.

class Post(models.Model):

    PRIVATE = 'private'
    ANOTHER_AUTHOR = 'author'
    FRIENDS = 'friend'
    FOAF = 'friendsOfFriends'
    SERVERONLY = 'friendsOwnHost'
    PUBLIC = 'public'

    visFriendlyString = {
        PRIVATE: 'Private',
        ANOTHER_AUTHOR: 'Another Author',
        FRIENDS: 'Friends',
        FOAF: 'Friends of Friends',
        SERVERONLY: 'Server Only',
    }

    PLAIN_TEXT = 'text/plain'
    MARK_DOWN = 'text/x-markdown'


    post_id = models.AutoField(primary_key=True);
    text = models.TextField()
    visibility = models.CharField(max_length=20,
                                  default=PUBLIC)

    mime_type = models.CharField(max_length=100,
                                 default=PLAIN_TEXT)

    publication_date = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)


    def __unicode__(self):
        return "id: %s\ntext: %s" % (self.post_id, self.text)

    @staticmethod
    def deletePost(postId):
        # this should delete the entries in the relational table as well according to the docs
        Post.objects.filter(post_id=postId).delete()

    def getVisibilityTypes(self):
        return self.visFriendlyString

    @staticmethod
    def isViewable(post, author):
        return True

    @staticmethod
    def getVisibleToAuthor(author):
        return []


    @staticmethod
    def getByAuthor(author):
        return AuthoredPost.objects.filter(author=author)


class AuthoredPost(models.Model):
    author = models.ForeignKey(Author)
    post = models.ForeignKey(Post)

    def __unicode__(self):
        return "post %s made by %s" % (self.author.user, self.post.post_id)

class VisibleToAuthor(models.Model):
    post = models.ForeignKey(Post)
    visibleAuthor = models.ForeignKey(Author)

    def __unicode__(self):
        return "specific post %s visible to only %s" % (self.post.post_id, self.visibleAuthor.user)