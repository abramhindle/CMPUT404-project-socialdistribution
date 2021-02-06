from django.db import models
import uuid

# Related Model
from api.models.author import Author

class Follower(models.Model):
    # Unique ID of this follower Record
    follow_id  = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    
    # The person who want to follow
    follower   = models.ForeignKey(Author, null=False, on_delete=models.CASCADE, related_name="follower")

    # The person who is being followed( The person who should get the request )
    followee   = models.ForeignKey(Author, null=False, on_delete=models.CASCADE, related_name="followee")
    
    url        = models.URLField()

    # NOTE: Not exactly sure how connection to other servers will work but would we need to store author urls?
    # Not sure yet so lets just hold off but might be needed, unless we can populate our author table with remote
    # Authors, in which case this table is fine as-is.

    published  = models.DateField(auto_now_add=True)

