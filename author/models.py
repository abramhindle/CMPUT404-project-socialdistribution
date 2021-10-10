from django.db import models

class Author(models.Model):
    authorID = models.CharField(max_length=32, primary_key=True)
    email = models.EmailField()
    passwordHash = models.TextField()
    host = models.SlugField()


class Follow(models.Model):
    fromAuthor = models.ForeignKey(Author, on_delete=models.CASCADE)
    toAuthor = models.ForeignKey(Author, on_delete=models.CASCADE)
    date = models.DateTimeField()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['fromAuthor', 'toAuthor'], name='Unique Follows')
        ]


class Inbox(models.Model):
    authorID = models.ForeignKey(Author, on_delete=models.CASCADE)
    # inboxType indicates if it is a like, comment, or new post
    inboxType = models.CharField(max_length=8)
    fromAuthor = models.ForeignKey(Author, on_delete=models.CASCADE)
    date = models.DateTimeField()
    postID = models.ForeignKey('post.Post', on_delete=models.CASCADE, null=True, blank=True)
