from django.db import models
from api.models.authorModel import Author

class FriendRequest(models.Model):
    # FriendRequest Type
    type = models.CharField(null=True, blank=True, default='follow', max_length=50)
    # FriendRequest Summary
    summary = models.CharField(null=True, blank=True, max_length=100)
    # FriendRequest Actor
    actor = models.ForeignKey(Author, on_delete=models.CASCADE, null=True, related_name='friend_request_actor')
    # FriendRequest Object
    object = models.ForeignKey(Author, on_delete=models.CASCADE, null=True, related_name='friend_request_object')

    def __init__(self, *args, **kwargs):
        super(FriendRequest, self).__init__(*args, **kwargs)
        if (self.actor != None) and (self.object != None):
            # set summary to format specified in the project specifications
            self.summary = self.actor.displayName + ' wants to follow ' + self.object.displayName
