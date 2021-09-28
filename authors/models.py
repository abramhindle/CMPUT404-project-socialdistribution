import uuid
from django.db import models
from django.urls import reverse 
from django.contrib.auth.models import User

# Create your models here.
class Author(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    user = models.OneToOneField(User, on_delete=models.CASCADE) # one2one with django user
    friends = models.ManyToManyField("self") # bidirectional/symmetrical by default

    display_name = models.CharField(max_length=30) # maximum 30 chars for display name
    url = models.URLField() # the url to the author profile
    host = models.URLField() # the host server node url, ours is https://social-distance-api.herokuapp.com/

    # following: Authors, added by related name, see AuthorFollowingRelation
    # followers: Authors, added by related name, see AuthorFollowingRelation

    def get_absolute_url(self):
        return reverse('author-detail', args=[str(self.id)])

class AuthorFriendRequest(models.Model):
    """
    Request from an author who wants to befriend/follow another author.
    Once accepted, both authors can see each others' friend posts and previous friend posts.
    """
    # author who is sending the friend/following request
    author_from = models.ForeignKey("Author", related_name="friend_requests_sent", on_delete=models.CASCADE)
    # author who is receiving the request
    author_to = models.ForeignKey("Author", related_name="friend_requests_received", on_delete=models.CASCADE)

