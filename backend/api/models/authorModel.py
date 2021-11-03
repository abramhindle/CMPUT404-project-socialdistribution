from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid

# Author Model
# Extends from the django user model upon account registration
class Author(AbstractUser):
    # User URL ID
    authorID = models.URLField(primary_key=True, default=uuid.uuid4)
    # User displayName
    displayName = models.CharField(blank=True, max_length=100)
    # User's personal URL
    url= models.URLField(null=True)
    # User host URL
    host = models.URLField(max_length=150)
    # User's Github URL
    github = models.URLField()
    

    # def __init__(self, *args, **kwargs):
    #     super(Author, self).__init__(*args, **kwargs)
    #     if self.host != None:
    #         # make sure host ends with a '/'
    #         self.host += '/' if (not self.host.endswith('/')) else ''

    #         # set id and url to format specified in the project specifications
    #         self.id = self.host +  '/' + str(self.id)
    #         self.url = self.id
