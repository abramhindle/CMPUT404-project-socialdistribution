import uuid
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import User, UserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.base_user import BaseUserManager

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from PIL import Image


# Have to do this because in settings.py USER_AUTH_MODEL is set to Author.
# Because of that, the admin page switches to requiring an email instead of user name.
class CustomUserManager(BaseUserManager):
    # Over riding create_superuser as otherwise the default implementation
    # doesn't work with the custom model.
    def create_superuser(self, email, password=None):
        user = self.model(
            email=self.normalize_email(email),
        )
        user.set_password(password)
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.save()
        return user


# Need to subclass PermissionMixin to have the properties of admin accounts.
class Author(AbstractBaseUser, PermissionsMixin):
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
    email = models.EmailField(unique=True)
    firstName = models.CharField(max_length=50)
    lastName = models.CharField(max_length=50)
    displayName = models.CharField(max_length=100)
    bio = models.TextField()
    host = models.URLField(max_length=255)
    github = models.URLField(max_length=255)
    profile_img = models.FileField(default='temp.jpg', upload_to='profile/')
    password = models.CharField(max_length=255, default="changeme")

    objects = CustomUserManager()
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'

    # Not sure if this is the right appraoch or we should be storing this field
    @property
    def url(self):
        # In the future use url reverse
        # reverse('author', args=[str(id)])
        return("%s/author/%s" % (self.host, self.id))

    def __str__(self):
        return("%s %s" % (self.firstName, self.lastName))

    def serialize(self):
        fields = ["id", "email", "firstName", "lastName", "displayName", "bio",
                  "host", "github", "profile_img"]
        author = dict()
        for field in fields:
            author[field] = str(getattr(self, field))

        return author

# A model to store authors request to follow another author
# If table contains (1,2) but not (2,1) then it is a request by 1 to befriend 2
# If table contains (1,2) and (2,1) then 1 and 2 are friends and request was
# accepted.
class AuthorFriend(models.Model):
    author = models.ForeignKey(Author, related_name="AuthorFriend_author",
                               on_delete=models.CASCADE, null=True)
    friend = models.ForeignKey(Author, related_name="AuthorFriend_friend",
                               on_delete=models.CASCADE, null=True)

    class Meta:
        unique_together = ('author', 'friend')
