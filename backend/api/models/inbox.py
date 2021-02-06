from django.db import models
import uuid

# Related Models
from api.models.author import Author
from api.models.post import Post
from api.models.comment import Comment
from api.models.like import Like

MessageTypes = [
    ('post', 'post'),
    ('comment', 'comment'),
    ('like', 'like'),
]

class Inbox(models.Model):
    # Unique ID of this inbox record
    item_id     = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)


    # Whose inbox this pertains to
    author_id   = models.ForeignKey(Author, on_delete=models.CASCADE)
    
    # What type of message is in the inbox
    # THIS SHOULD NEVER BE NULL, BUT WE ALSO DONT HAVE A DEFAULT VALUE
    messageType = models.TextField(null=True, choices=MessageTypes) 

    # Not sure how to combine all of the possible foreign keys so I will leave it up to business logic
    # TO be a valid inbox item, it should be checked that at least one of the following id's is not null
    post_id     = models.ForeignKey(Post, on_delete=models.CASCADE, blank=True, null=True)
    comment_id  = models.ForeignKey(Comment, on_delete=models.CASCADE, blank=True, null=True)
    like_id     = models.ForeignKey(Like, on_delete=models.CASCADE, blank=True, null=True)

    messageUrl  = models.URLField()

    # When this record was created
    published   = models.DateField(auto_now_add=True)
