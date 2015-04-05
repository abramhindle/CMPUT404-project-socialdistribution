from django.conf import settings
from django.db import models

from django.contrib.auth.models import User
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist

import uuid as hash_id


class Author(models.Model):

    """Represents a author, which is a primary user in socialdistribution.

    Some of the things an author can do include creating and sharing posts,
    adding friends, managing their profile, and more.

    An author has a one to one relationship with Django's User, which will
    be used for login and authentication.

    An author will also be tied to one GitHub account, which will be used to
    retrieve their GitHub feed.
    """
    uuid = models.CharField(max_length=256, unique=True, default=hash_id.uuid4)

    user = models.OneToOneField(User, primary_key=True)
    github_user = models.CharField(max_length=128, blank=True)

    host = models.CharField(max_length=128, default=settings.LOCAL_HOST)

    # The url is information we gather from remote authors during friend
    # requests, we may or may not use it.
    url = models.CharField(max_length=256, blank=True)

    # An etag is used to retrieve events in GitHub. Normally, there is a limit
    # to the number of API calls you can make to GitHub. This limit is set to
    # 60, so it can be an issue. If we specify the etag in the header, and the
    # events haven't changed since the previous query, this won't count towards
    # our rate limit.
    github_etag = models.CharField(max_length=64, blank=True)

    def __unicode__(self):
        return self.user.username

    @classmethod
    def create(self, user, github_user=None, host=settings.LOCAL_HOST,
               uuid=hash_id.uuid4, url=None):
        author = cls(user=user,
                     github_user=github_user,
                     host=host,
                     uuid=uuid,
                     url=url)
        return author

    def get_host(self):
        return self.host

    def get_url(self):
        return self.url

    def get_username(self):
        """Trim the host from remote author usernames."""
        split = self.user.username.split('__', 1)
        if len(split) > 1:
            return split[1]
        else:
            return self.user.username

    def get_uuid(self):
        """Trim the host from remote author usernames."""
        return self.uuid

    def get_json_obj(self):
        authorJson = {}
        authorJson['id'] = unicode(self.get_uuid())
        authorJson['host'] = unicode(self.host)
        authorJson['displayname'] = unicode(self.get_username())
        authorJson['url'] = unicode(self.host + "/author/" + self.get_uuid())

        return authorJson

    @staticmethod
    def get_author_with_username(name):
        user = User.objects.get(username=name)
        return Author.objects.get(user=user)

class FriendRequest(models.Model):
    """Represents a friend request."""
    
    id = models.AutoField(primary_key=True)
    requester = models.ForeignKey(Author, related_name='friend_requests_r')
    requestee = models.ForeignKey(Author, related_name='friend_requests_s')
    frStatus = models.BooleanField(default = False)
    requestStatus = models.BooleanField(default= False)
    followStatus = models.BooleanField(default = False)

    @staticmethod
    def received_requests(author):
        """Returns a list of authors the author got requests from."""
        pendingList = []
        requests = (FriendRequest.objects.filter(requestee=author)
                    .filter(requestStatus=True))
        for request in requests:
            pendingList.append(request.requester)
        return pendingList

    @staticmethod
    def sent_requests(author):
        """Returns a list of authors requested to be friends with."""
        requestList = []
        requests = (FriendRequest.objects.filter(requester=author)
                    .filter(requestStatus=True))
        for request in requests:
            requestList.append(request.requestee)
        return requestList

    @staticmethod
    def get_friends(author):
        """Returns the user's friends in a list."""
        friends = []
        requests = FriendRequest.objects.filter((Q(requestee=author) |
                                                 Q(requester=author)) &
                                                Q(frStatus=True))
        for friend in requests:
            if friend.requestee == author:
                # friends.append(friend.requester.user.username)
                friends.append(friend.requester)
            else:
                # friends.append(friend.requestee.user.username)
                friends.append(friend.requestee)
        return friends

    @staticmethod
    def is_friend(author1, author2):
        """Returns true if the two author are friends, false otherwise."""
        friend = FriendRequest.objects.filter(Q(requestee=author1,
                                                requester=author2,
                                                frStatus=True)
                                              | Q(requestee=author2,
                                                  requester=author1,
                                                  frStatus=True))
        if friend.exists():
            return True
        return False

    @staticmethod
    def follow(author1, author2):
        if FriendRequest.is_following(author1, author2):
            return False
        entry = FriendRequest(requester=author1, requestee=author2, followStatus = True)
        entry.save()
        return True

    @staticmethod
    def is_following(author1, author2):
        requestObj = FriendRequest.objects.filter(Q(requester=author1,
                                                    requestee=author2)
                                                & (Q(followStatus = True)
                                                | Q(frStatus = True)))
        if requestObj.exists() | FriendRequest.is_friend(author1, author2):
            return True
        return False

    @staticmethod
    def make_request(author1, author2):
        """Author1 sends a friend request to author2."""
        check = FriendRequest.objects.filter(Q(requester=author1,
                                                requestee=author2)
                                            | Q(requester=author2,
                                                  requestee=author1)
                                            & (Q(requestStatus=True)
                                            |  Q(frStatus=True)))
        if check.exists():
            return False
        try:
            requestObj = FriendRequest.objects.get(Q(requester=author1,
                                                     requestee=author2))
            requestObj.requestStatus = True
            requestObj.save()
            return True
        except:
            requestObj = FriendRequest(
                requester=author1, requestee=author2, requestStatus=True)
            requestObj.save()
            return True

    @staticmethod
    def accept_request(author1, author2):
        """Author2 accepts the request of author1."""
        try:
            requestObj = FriendRequest.objects.get(requestee=author2,
                                                   requester=author1,
                                                   requestStatus=True)
        except ObjectDoesNotExist:
            return False
        requestObj.frStatus = True
        requestObj.requestStatus = False
        requestObj.save()
        return True

    @staticmethod
    def reject_request(author1, author2):
        """Author2 rejects the request of author1."""
        try:
            requestObj = FriendRequest.objects.get(requestee=author2,
                                                   requester=author1,
                                                   requestStatus=True)
        except ObjectDoesNotExist:
            return False
        requestObj.requestStatus = False
        requestObj.save()
        return True

    @staticmethod
    def get_status(user1, user2):
        """Identifies whether the two users are friends.

        Returns true if the users are friends, false if user1 is following
        user2 (ie. user1 requested a friendship to user2), and None if there's
        no relationship.
        """
        status = (FriendRequest.objects.filter(requester=user1)
                  .filter(requestee=user2))
        if status.exists():
            for u in status:
                return u.status
        return None

    @staticmethod
    def unfriend(author1, author2):
        print(author1)
        print(author2)
        if FriendRequest.is_friend(author1, author2):
            print("friends")
            try:
                friend = FriendRequest.objects.get(Q(requestee=author1,
                                                    requester=author2,
                                                    frStatus=True)
                                                | Q(requestee=author2,
                                                    requester=author1,
                                                    frStatus=True))
                print("found")
                friend.frStatus = False
                friend.save()
                return True
            except ObjectDoesNotExist:
                return False
        return False


    def __unicode__(self):
        return "%s, %s" % (self.requestee, self.requester)
