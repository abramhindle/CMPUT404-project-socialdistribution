import uuid

from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save

from social.app.models.node import Node


class Author(models.Model):
    user = models.OneToOneField(User, related_name='user')

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    displayName = models.CharField(max_length=512)

    ### Optional Attributes

    # https://github.com/join
    github = models.URLField(default='', blank=True)

    bio = models.TextField(default='', blank=True)

    ### Meta Attributes
    activated = models.BooleanField(default=False)

    node = models.ForeignKey(Node, on_delete=models.CASCADE)

    followed_authors = models.ManyToManyField(
        'self',
        symmetrical=False,
        # Ensures no backwards relation is created
        # No need to for an author to see who follows them
        related_name='+',
        blank=True)

    outgoing_friend_requests = models.ManyToManyField(
        'self',
        symmetrical=False,
        related_name='incoming_friend_requests',
        blank=True
    )

    friends = models.ManyToManyField('self', blank=True)

    def get_id_url(self):
        return '%sauthors/%s/' % (self.node.service_url, str(self.id))

    def follows(self, author):
        return self != author and len(self.followed_authors.filter(id=author.id)) > 0

    def friends_with(self, author):
        return self != author and len(self.friends.filter(id=author.id)) > 0

    def has_outgoing_friend_request_for(self, author):
        return self != author and len(self.outgoing_friend_requests.filter(id=author.id)) > 0

    def has_incoming_friend_request_from(self, author):
        return self != author and len(self.incoming_friend_requests.filter(id=author.id)) > 0

    def can_follow(self, author):
        return not (
            self == author
            or not self.activated
            or not author.activated
            or self.follows(author)
        )

    def can_send_a_friend_request_to(self, author):
        return not (
            self == author
            or not self.activated
            or not author.activated
            or self.friends_with(author)
            or self.has_outgoing_friend_request_for(author)
            or self.has_incoming_friend_request_from(author)
        )

    def add_friend_request(self, author):
        self.outgoing_friend_requests.add(author)
        self.followed_authors.add(author)

    def accept_friend_request(self, author):
        if self.incoming_friend_requests.filter(id=author.id):
            self.incoming_friend_requests.remove(author)
            self.friends.add(author)
        else:
            raise Exception("Attempted to accept a friend request that does not exist.")

    def __str__(self):
        return '%s, %s (%s)' % (self.user.last_name, self.user.first_name, self.displayName)


def create_profile(sender, **kwargs):
    user = kwargs["instance"]
    if not user.is_staff and kwargs["created"]:
        user_profile = Author(user=user)
        user_profile.displayName = user_profile.user.first_name + ' ' + user_profile.user.last_name
        user_profile.node = Node.objects.get(local=True)
        user_profile.save()


post_save.connect(create_profile, sender=User)

User.profile = property(lambda u: Author.objects.get_or_create(user=u)[0])
