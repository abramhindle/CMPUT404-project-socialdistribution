import uuid
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import User

# from django.core.urlresolvers import reverse

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver




class Author(models.Model):
    """
    definition of author from 'example-article.json'
    "author":{
    "id":"http://127.0.0.1:5454/author/1d698d25ff008f7538453c120f581471",
    "host":"http://127.0.0.1:5454/",
    "displayName":"Greg Johnson",
    "url":"http://127.0.0.1:5454/author/1d698d25ff008f7538453c120f581471",
    "github":"http://github.com/gjohnson",
    # Optional attributes
    "github": "http://github.com/lara",
    "firstName": "Lara",
    "lastName": "Smith",
    "email": "lara@lara.com",
    "bio": "Hi, I'm Lara"
    }
    """
    # id is previously defined along with the host which seems odd. For now,
    # only defined id as the uuid, may need to change in the future to
    # match specs.
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField()
    firstName = models.CharField(max_length=50)
    lastName = models.CharField(max_length=50)
    displayName = models.CharField(max_length=100)
    bio = models.TextField()
    host = models.URLField(max_length=255)
    github = models.URLField(max_length=255)
    profile_img = models.FileField(default='temp.jpg', upload_to='profile/')

    # Not sure if this is the right appraoch or we should be storing this field
    @property
    def url(self):
        # In the future use url reverse
        # reverse('author', args=[str(id)])
        return("%s/author/%s" % (self.host, self.id))

    def __str__(self):
        return("%s %s" % (self.firstName, self.lastName))


# A model to handle friend requests
# Each friend request is stored in the AuthorFriendRequest model
# and updates request_accepted to True once recipient author confirms request
# The AuthorFriendRequest model is redundant and does not
# need to be present if we do not want to track friend requests
# It is sufficient to add entries to AuthorFriend model.

class AuthorFriendRequest(models.Model):
    author = models.ForeignKey(Author, related_name="AuthorFriendRequest_author",
                               on_delete=models.CASCADE, null=True)
    friend = models.ForeignKey(Author, related_name="AuthorFriendRequest_friend",
                               on_delete=models.CASCADE, null=True)
    request_accepted = models.BooleanField(default=False, null=False)


# A model to store authors request to follow another author
# If table contains (1,2) but not (2,1) then it is a request by 1 to befriend 2
# If table contains (1,2) and (2,1) then 1 and 2 are friends and request was
# accepted.

class AuthorFriend(models.Model):
    author = models.ForeignKey(Author, related_name="AuthorFriend_author",
                               on_delete=models.CASCADE, null=True)
    friend = models.ForeignKey(Author, related_name="AuthorFriend_friend",
                               on_delete=models.CASCADE, null=True)

@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    print("N HERE")
    logging.debug("HERE")
    if created:
        print("created")
        Profile.objects.create(author=instance)
    instance.profile.save()
