from django.db import models
from .postModel import Post
from api.models.authorModel import Author
import uuid

class Comment(models.Model):
    ContentTypes = (
        ("text/plain", "Plain"),
        ("text/markdown", "Markdown"),
        ('application/base64', 'Application'),
        ('image/png;base64'  , 'ImagePNG'),
        ('image/jpeg;base64' , 'ImageJPEG')
    )
    # Comment ID  
    commentID = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    # Comment Post ID 
    commentPostID = models.ForeignKey(Post, on_delete=models.CASCADE)
    # Comment content(data)
    content = models.TextField()
    # Comment Type
    contentType = models.TextField(choices=ContentTypes, default="text/plain", null=False)
    # Comment published date
    published = models.DateTimeField(auto_now_add=True)
    # Comment URL
    url = models.URLField()
    # Comment Author. [The Author of the comment]
    commentAuthorID = models.ForeignKey(Author, on_delete=models.CASCADE)

    def __str__(self):
        return (f"The following data for this comment are ,Post:{self.commentPostID},Author:{self.commentAuthor},ContentType:{self.contentType},content: {self.content}")