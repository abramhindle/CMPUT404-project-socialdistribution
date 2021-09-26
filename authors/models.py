import uuid
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Author(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    user = models.OneToOneField(User, on_delete=models.CASCADE) # one2one with django user
    friends = models.ManyToManyField("self") # bidirectional/symmetrical by default

    displayName = models.CharField(max_length=30) # maximum 30 chars for display name
    url = models.URLField() # the url to the author profile
    host = models.URLField() # the host server node url, ours is https://social-distance-api.herokuapp.com/

    # following: Authors, added by related name, see AuthorFollowingRelation
    # followers: Authors, added by related name, see AuthorFollowingRelation

class AuthorFollowingRelation(models.Model):
    # whoever is following: he/she can access his following people with author.following.all()
    follower = models.ForeignKey("Author", related_name="following", on_delete=models.CASCADE)
    # whomever is being followed: he/she can access his followers with author.followers.all()
    following = models.ForeignKey("Author", related_name="followers", on_delete=models.CASCADE)
