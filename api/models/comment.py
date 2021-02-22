from django.db import models
import uuid

# Related Model
from api.models.post import Post
from api.models.author import Author

# List of tuples containing the content-types that are handled by this model
ContentTypes = [
    ('text/markdown'     , 'text/markdown'),
    ('text/plain'        , 'text/plain'),
    ('application/base64', 'application/base64'),
    ('image/png;base64'  , 'image/png;base64'),
    ('image/jpeg;base64' , 'image/jpeg;base64')
]


class Comment(models.Model):
    # Specific reference to this comment
    comment_id  = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)

    # Comment refers to a post
    post_id     = models.ForeignKey(Post, on_delete=models.CASCADE)

    # What the actual comment is
    content     = models.TextField()

    # Type of the comment
    contentType = models.TextField(null=False, choices=ContentTypes, default='text/plain')

    # When the comment was created
    published   = models.DateField(auto_now_add=True)

    # Comment Author, if the author is deleted: delete all comments made by this user?? (NOT SURE ABOUT CASCADE HERE)
    C_author_id   = models.ForeignKey(Author, on_delete=models.CASCADE)
    
    # Full url of this comment
    url         = models.URLField()
