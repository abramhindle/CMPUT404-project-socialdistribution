from django.db import models

from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models import Q

import uuid

class Author(models.Model):
    """Represents a author, which is a primary user in socialdistribution.

    Some of the things an author can do include creating and sharing posts,
    adding friends, managing their profile, and more.

    An author has a one to one relationship with Django's User, which will
    be used for login and authentication.

    An author will also be tied to one GitHub account, which will be used to
    retrieve their GitHub feed.
    """
    uuid = models.CharField(max_length=40, unique=True, default=uuid.uuid4)

    user = models.OneToOneField(User, primary_key=True)
    github_user = models.CharField(max_length=128, blank=True)

    host = models.CharField(max_length=128, default='localhost:8000')

    # An etag is used to retrieve events in GitHub. Normally, there is a limit
    # to the number of API calls you can make to GitHub. This limit is set to
    # 60, so it can be an issue. If we specify the etag in the header, and the
    # events haven't changed since the previous query, this won't count towards
    # our rate limit.
    github_etag = models.CharField(max_length=64, blank=True)

    def __unicode__(self):
        return self.user.username

    @classmethod
    def create(self, user, github_user=None, host='localhost:8000'):
        author = cls(user=user, github_user=github_user, host=host)
        return author

class FriendRequest(models.Model):
    """
    Represents a friend request, includes the minimal stuff required..for now

    """
    id = models.AutoField(primary_key=True)
    requester = models.ForeignKey(User, related_name='friend_requests_r')
    requestee = models.ForeignKey(User, related_name='friend_requests_s')
    status = models.BooleanField(default = False)
    
    def pending_requests(author):
        print(author)
        #authorObject = Author.objects.get(pk = author)
        requests = FriendRequest.objects.filter(requestee=author).filter(status = False)
        #print("ao" + authorObject)
        print(requests)
        return(requests)

    def get_status(user1, user2):
        """
        Returns true if the users are friends, false if user1 is following user2 (ie. user1 
        requested a friendship to user2), and none if there's no relationship
        """
        print(user1)
        print(user2)
        status = FriendRequest.objects.filter(requester=user1).filter(requestee=user2)
        if status.exists() :
            print(status)
            for u in status :
                return u.status
        return None
        """
        if status.exists() :
            for u in status :
                print(u.requestStatus)
            #status2 = FriendRequest.objects.filter(requester__author = status)
            #print(status2)
                if u.requestStatus == False:
                    return "isFollowing"
                if u.requestStatus == True:
                    return "friend"
        else :
            status = FriendRequest.objects.filter(requester=user2).filter(requestee=user1)
            if status.exists() :
                for u in status :
                    if u.requestStatus == False:
                        return "beingFollowed"
        return "stranger"
        """

    def __unicode__(self):
        return "%s, %s" % (self.requestee, self.requester)
