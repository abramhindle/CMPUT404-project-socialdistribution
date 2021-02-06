from django.db import models
import uuid

from django.db.models.deletion import CASCADE

# Related Models
from api.models.post import Post
from api.models.comment import Comment
from api.models.author import Author

LikeTypes = [
    ('post'   , 'post'),
    ('comment', 'comment')
]

class Like(models.Model):
    # Unique reference to this like
    like_id    = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    
    # not exactly sure how to combine this into a single source id, i have made them nullable
    # in the meantime
    post_id    = models.ForeignKey(Post, on_delete=models.CASCADE,blank=True, null=True)
    comment_id = models.ForeignKey(Comment, on_delete=models.CASCADE, blank=True, null=True)
    
    # Id of the user who actually liked the comment or post, if the user is deleted, their likes should also go
    L_author_id  = models.ForeignKey(Author, on_delete=models.CASCADE)

    # Text choice determining whether a post or a comment has been liked
    like_type  = models.TextField(choices=LikeTypes)

    url        = models.URLField()
