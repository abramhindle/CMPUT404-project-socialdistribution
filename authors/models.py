import uuid
from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse 
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

# Create your models here.
class Author(models.Model):
    id = models.CharField(primary_key=True, editable=False, default=uuid.uuid4, max_length=80)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True) # one2one with django user
    friends = models.ManyToManyField('Author', blank=True, symmetrical=True) # bidirectional/symmetrical by default, allow empty

    display_name = models.CharField(max_length=30, blank=True) # maximum 30 chars for display name
    github_url = models.URLField(null=True, blank=True) # the url to the author github profile
    url = models.URLField(editable=False) # the url to the author profile
    host = models.URLField(editable=False) # the host server node url, ours is https://social-distance-api.herokuapp.com/

    # following: Authors, added by related name, see AuthorFollowingRelation
    # followers: Authors, added by related name, see AuthorFollowingRelation

    # used by serializer
    def get_public_id(self):
        return self.url or self.id

    # used internally
    def get_absolute_url(self):
        return reverse('author-detail', args=[str(self.id)])

    # clean up whenever trying to validate model object
    def clean(self):
        # enforce author-user one2one
        if self.user is None:
            raise ValidationError(_('Author object has to have a User object linked.'))

        # default display_name to username
        if not self.display_name:
            self.display_name = self.user.username

    # used by serializer
    def update_fields_with_request(self, request):
        self.url = request.build_absolute_uri(self.get_absolute_url())
        self.host = request.build_absolute_uri('/') # points to the server root
        self.save()

class Follow(models.Model):
    """
    Relation that represents the current Author, A, being followed by another author, B
    followee: A
    follower: B

    """

    # Author who is being followed by the follower. corresponds to Author.follower.all()
    followee = models.ForeignKey(Author, related_name="followers", null=False, on_delete=models.CASCADE)

    # URL of Author who is following the followee
    follower = models.ForeignKey(Author, related_name="followings", null=False, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['followee', 'follower'], name='unique_follower')
        ]


class FriendRequest(models.Model):
    """
    Request from an author who wants to befriend/follow another author.
    Once accepted, both authors can see each others' friend posts and previous friend posts.
    """
    summary = models.CharField(max_length=200)
    # author who is sending the friend/following request
    actor = models.ForeignKey("Author", related_name="friend_requests_sent", on_delete=models.CASCADE)
    # author who is receiving the request
    object = models.ForeignKey("Author", related_name="friend_requests_received", on_delete=models.CASCADE)


class InboxObject(models.Model):

    # the target author, whom the object is sent to.
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='inbox_objects')
    # https://docs.djangoproject.com/en/3.2/ref/contrib/contenttypes/#generic-relations
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True)
    object_id = models.CharField(max_length=100, null=True)
    content_object = GenericForeignKey('content_type', 'object_id')