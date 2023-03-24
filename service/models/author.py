from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
import uuid
from django.conf import settings

# Create your models here.

class MyUserManager(UserManager):
    def create_user(self, username, displayName=None, github=None, profileImage=None, email=None, password=None, **extra_fields):
        user = self.model(
            username=username,
            displayName=displayName,
            github=github,
            profileImage=profileImage,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, username, displayName=None, github=None, profileImage=None, email=None, password=None, **extra_fields):    
        user = self.create_user(
            username,
            password=password,
            displayName=displayName,
            github=github,
            profileImage=profileImage,
        )

        user.is_staff = True
        user.is_superuser = True
        user.is_active = True

        user.save(using=self._db)
        return user
    
def newId():
    return f"{settings.DOMAIN}/authors/{uuid.uuid4()}"

class Author(AbstractUser):
    class Meta:
        verbose_name = "Author"

    username = models.CharField(max_length=32, unique=True)
    is_active = models.BooleanField(default=False)
    is_local = models.BooleanField(default=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['displayName', 'github', 'profileImage']

    objects = MyUserManager()


    _id = models.URLField(primary_key=True, default=newId, editable=False)
    host = models.URLField(default=settings.DOMAIN, blank=True)
    displayName = models.CharField(max_length=128)
    github = models.URLField()
    profileImage = models.URLField()

    followers = models.ManyToManyField('Author', blank=True)

    def toJSON(self):
        return {
            "type": "author",
            "id": self._id,
            "host": self.host,
            "displayName": self.displayName,
            "url": self._id, #dont really know what this is for...
            "github": self.github,
            "profileImage": self.profileImage,
    }

    def toObject(self, json_object):
        self._id = json_object["id"]
        self.host = json_object["host"]
        self.displayName = json_object["displayName"]
        self.url = json_object["url"]
        self.github = json_object["github"]
        self.profileImage = json_object["profileImage"]

    
