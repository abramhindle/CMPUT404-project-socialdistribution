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
    def received_requests(author):
        """
        returns a list of authors the author got requests from
        """
        pendingList = []
        requests = FriendRequest.objects.filter(requestee=author).filter(status = False)
        for request in requests:
            pendingList.append(request.requester)  
        return(pendingList)

    @staticmethod
    def sent_requests(author):
        """
        returns a list of authors the author requested to be friends with 
        """
        requestList = []
        requests = FriendRequest.objects.filter(requester=author).filter(status = False)
        for request in requests:
            requestList.append(request.requestee)  
        return(requestList)

    def is_following(author1, author2):
        """
        returns true if author1 is following author2, false otherwise (ie.True if author1 requested a friendship 
        to author2)
        """
        follow = FriendRequest.objects.filter(requester=author1).filter(requestee=author2).filter(status = False)
        if follow.exists() :
            return True
        return False


    @staticmethod
    def get_friends(author):
        """
        returns the user's friends in a list
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
        return friends


    def is_friend(author1, author2):
        """
        returns true if they're friends, false otherwise
        """
        friend = FriendRequest.objects.filter(Q(requestee=author1, requester = author2, status = True) | Q(requestee=author2, requester = author1, status = True))
        if friend.exists():
            return True
        return False

    def make_request(author1, author2):
        """
        author1 sends a friend request to author2
        """
        follow = FriendRequest.objects.filter(Q(requester=author1, requestee=author2) | (Q(requester=author2, requestee=author1)))
        if follow.exists() :
            return False
        newEntry = FriendRequest(requester = author1, requestee = author2)
        newEntry.save()
        return True

    def accept_request(author1, author2):
        """
        author1 accepts the request of author2
        """
        try:
            requestObj = FriendRequest.objects.get(requestee = author1, requester = author2, status = False)
        except ObjectDoesNotExist:
            return False
        requestObj.status = True
        requestObj.save()
        return True

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
