from django.db import models
from api.models.authorModel import Author

class Like(models.Model):
    # Like Context
    context = models.CharField(default='https://www.w3.org/ns/activitystreams', max_length=100)
    # Like Summary
    summary = models.CharField(null=True, blank=True, max_length=500)
    # Like Type
    type = models.CharField(default='like', max_length=100)
    # Like Author
    author = models.ForeignKey(Author, on_delete=models.CASCADE, null=True, related_name='like_author')
    # Like Object
    object = models.URLField(null=True, blank=True)
    # Like Date
    date = models.DateTimeField(null=True, blank=True, auto_now_add=True)

    def __init__(self, *args, **kwargs):
        super(Like, self).__init__(*args, **kwargs)
        if (self.object != None) and (self.object[-1] == '/'):
            # make sure object does not end with a '/'
            self.object = self.object[:-1]
