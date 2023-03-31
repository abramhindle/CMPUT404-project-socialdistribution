from django.db import models
from django import forms
from service.models.author import Author
import uuid
from django.conf import settings
from datetime import datetime, timezone

class Follow(models.Model): # list of an author's followers
    _id = models.URLField(primary_key=True, default=None)
    actor = models.ForeignKey(Author, on_delete=models.CASCADE, related_name="actor") #this is the person DOING THE FOLLOWING -> i.e. author of the follow request
    object = models.ForeignKey(Author, on_delete=models.CASCADE, related_name="object") #this is the person being FOLLOWED!

    published = models.DateTimeField()

    def save(self, *args, **kwargs):
        self._id = self.create_follow_id(self.actor._id, self.object._id)
        self.published = datetime.now(timezone.utc)
        super(Follow, self).save(*args, **kwargs)

    @staticmethod
    def create_follow_id(object_id, actor_id): #uses the last uuid value from author id, and generates a custom post_id
        object_uuid = object_id.rsplit('/', 1)[-1]
        actor_uuid = actor_id.rsplit('/', 1)[-1]
        return f"{settings.DOMAIN}/authors/{actor_uuid}/follower-request/{object_uuid}" #object = person being followed

    def toJSON(self):
        return {
            "type": "follow",
            "summary": f"{self.actor.displayName} wants to follow {self.object.displayName}",
            "actor": self.actor.toJSON(), #wants to follow
            "object": self.object.toJSON()
        }
    
    def __str__(self):
        return f"{self.actor.displayName}, {self.object.displayName}"