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

    @staticmethod
    def getAuthorWithUserName(name):
        user = User.objects.get(username=name)
        return Author.objects.get(user=user)

class FriendRequest(models.Model):
    """
    Represents a friend request, includes the minimal stuff required..for now
    such as: requester: the user who made the friend request
              requestee: person who got a friend request
              status: status of the request; false means requestee hasn't accepted
                        the request yet and true means they're friends

    """
    id = models.AutoField(primary_key=True)
    requester = models.ForeignKey(Author, related_name='friend_requests_r')
    requestee = models.ForeignKey(Author, related_name='friend_requests_s')
    status = models.BooleanField(default = False)

    @staticmethod
    def pending_requests(author):
        """
        returns a list of friend requests (the User's usernames)
        """
        requestList = []
        requests = FriendRequest.objects.filter(requestee=author).filter(status = False)
        for request in requests:
            requestList.append(request.requester.user.username)
        return(requestList)

    @staticmethod
    def get_friends(author):
        """
        returns the user's friends (the User's usernames) in a list
        """
        friends = []
        requests = FriendRequest.objects.filter((Q(requestee=author) | Q(requester=author)) & Q(status = True))
        for friend in requests:
            if friend.requestee == author:
                #friends.append(friend.requester.user.username)
                friends.append(friend.requester)
            else:
                #friends.append(friend.requestee.user.username)
                friends.append(friend.requestee)
        print("friends")
        print(friends)
        return friends

    @staticmethod
    def get_status(user1, user2):
        """
        Returns true if the users are friends, false if user1 is following user2 (ie. user1
        requested a friendship to user2), and none if there's no relationship
        """
        status = FriendRequest.objects.filter(requester=user1).filter(requestee=user2)
        if status.exists() :
            for u in status :
                return u.status
        return None

    def __unicode__(self):
        return "%s, %s" % (self.requestee, self.requester)
