from django.db import models

from django.contrib import messages
from django.contrib.auth.models import User


class Author(models.Model):
    """Represents a author, which is a primary user in socialdistribution.

    Some of the things an author can do include creating and sharing posts,
    adding friends, managing their profile, and more.

    An author has a one to one relationship with Django's User, which will
    be used for login and authentication.

    An author will also be tied to one GitHub account, which will be used to
    retrieve their GitHub feed.
    """
    user = models.OneToOneField(User, primary_key=True)
    github_user = models.CharField(max_length=128, blank=True)

    # An etag is used to retrieve events in GitHub. Normally, there is a limit
    # to the number of API calls you can make to GitHub. This limit is set to
    # 60, so it can be an issue. If we specify the etag in the header, and the
    # events haven't changed since the previous query, this won't count towards
    # our rate limit.
    github_etag = models.CharField(max_length=64, blank=True)

    def __unicode__(self):
        return self.user.username

    @classmethod
    def create(self, user, github_user=None):
        author = cls(user=user, github_user=github_user)
        return author

class FriendRequest(models.Model):
    """
    Represents a friend request, includes the minimal stuff required..for now
    """
    id = models.AutoField(primary_key=True)
    requester = models.ForeignKey(User, related_name='friend_requests_r')
    requestee = models.ForeignKey(User, related_name='friend_requests_s')
    requestStatus = models.BooleanField(default = False)
    
    def pending_requests(author):
        print(author)
        #authorObject = Author.objects.get(pk = author)
        requests = FriendRequest.objects.filter(requestee=author)
        #print("ao" + authorObject)
        print(requests)
        return(requests)
    

    def __unicode__(self):
        return "%s, %s" % (self.requestee.username, self.requester.username)
