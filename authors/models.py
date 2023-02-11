from django.db import models
import uuid

MAX_LENGTH = 100
SMALLER_MAX_LENGTH = 50

'''
{
"type": "authors",
"items": [ {"type":"author",...}, ...]
}
'''
class Authors(models.Model):
    type = models.CharField(max_length=SMALLER_MAX_LENGTH)
    


'''
{
"type": "author",
"id": ...
"host": ...
"displayName": ...
"url": ...
"github": ...
"profileImage": ...
}
'''

class Author(models.Model):
    type = models.CharField(max_length=SMALLER_MAX_LENGTH)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)  # ID of the author
    home_host = models.URLField() # the home host 
    display_name = models.CharField(max_length=MAX_LENGTH) # the display name
    profile_url = models.URLField(max_length=MAX_LENGTH) # url to the author's profile
    author_github = models.URLField(max_length=MAX_LENGTH) # HATEOS url for Github API
    profile_image = models.URLField(max_length=MAX_LENGTH) # Image from a public domain (or ImageField?)

    def __str__(self):
        # clearer description of object itself rather than Author(1) in admin interface
        return self.display_name