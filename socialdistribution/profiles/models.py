import uuid
from django.db import models
# from django.core.urlresolvers import reverse


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
    profile_img = models.FileField(default='temp.jpg',upload_to='profile/')

    # Not sure if this is the right appraoch or we should be storing this field
    @property
    def url(self):
        # In the future use url reverse
        # reverse('author', args=[str(id)])
        return("%s/author/%s" % (self.host, self.id))

    def __str__(self):
        return("%s %s" % (self.firstName, self.lastName))
