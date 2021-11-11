from django.db import models
from .postModel import Post
from api.models.authorModel import Author
import uuid

class Comment(models.Model):
    TEXT_PLAIN = "text/plain"
    TEXT_MARKDOWN = "text/markdown"

    ContentTypes = (
        (TEXT_PLAIN, "Plain"),
        (TEXT_MARKDOWN, "Markdown"),
    )

    # Comment Type
    type = models.CharField(default='comment', max_length=50)
    # Comment UUID 
    uuid = models.UUIDField(primary_key=True, null=False, default=uuid.uuid4, editable=False)
    # Comment ID
    id = models.URLField(null=True, blank=True)
    # Comment Author
    author = models.ForeignKey(Author, on_delete=models.CASCADE, null=True, related_name='comment_author')
    # Comment Post
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True, related_name='comment_post')
    # Comment Content
    comment = models.TextField(null=True, blank=True)
    # Comment Content Type
    contentType = models.CharField(null=False, choices=ContentTypes, default=TEXT_PLAIN, max_length=18)
    # Comment Published Date
    published = models.DateTimeField(null=True, blank=True, auto_now_add=True)

    def __init__(self, *args, **kwargs):
        super(Comment, self).__init__(*args, **kwargs)
        if self.post != None:
            # make sure host ends with a '/'
            self.post.id += '/' if (not self.post.id.endswith('/')) else ''

            # set id to format specified in the project specifications
            self.id = self.post.id + 'comments/' + str(self.uuid)
