from django.db import models
import uuid

class Author(models.Model):
    authorID = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    displayName = models.CharField(max_length=32)
    email = models.EmailField()
    passwordHash = models.TextField()
    host = models.URLField()

    def get_url(self):
        return self.host + "author/" + str(self.authorID)


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
