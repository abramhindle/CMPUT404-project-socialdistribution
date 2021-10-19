from django.db import models
import uuid
from django.contrib.auth.models import User

class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    authorID = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    displayName = models.CharField(max_length=32)
    host = models.URLField()
    github = models.URLField(null=True, blank=True)
    profileImage = models.URLField(null=True, blank=True)

    def get_url(self):
        return self.host + "service/author/" + str(self.authorID)


class Follow(models.Model):
    fromAuthor = models.ForeignKey(Author, on_delete=models.CASCADE, related_name="author_following")
    toAuthor = models.ForeignKey(Author, on_delete=models.CASCADE, related_name="author_being_followed")
    date = models.DateTimeField()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['fromAuthor', 'toAuthor'], name='Unique Follows')
        ]


class Inbox(models.Model):
    authorID = models.ForeignKey(Author, on_delete=models.CASCADE, related_name="inbox_owner")
    # inboxType indicates if it is a like, comment, or new post
    inboxType = models.CharField(max_length=8)
    fromAuthor = models.ForeignKey(Author, on_delete=models.CASCADE, related_name="sender")
    date = models.DateTimeField()
    postID = models.ForeignKey('post.Post', on_delete=models.CASCADE, null=True, blank=True)
