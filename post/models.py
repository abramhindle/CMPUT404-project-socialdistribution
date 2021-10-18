from django.db import models
import uuid

class Post(models.Model):
    postID = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    ownerID = models.ForeignKey('author.Author', on_delete=models.CASCADE)
    date = models.DateTimeField()
    content = models.TextField()
    isPublic = models.BooleanField()
    isListed = models.BooleanField()
    hasImage = models.BooleanField()
    contentType = models.CharField(max_length=16)
    host = models.URLField()

    def get_url(self):
        return self.host + "author/" + str(self.ownerID.authorID) + "/post/" + str(self.postID)


class Like(models.Model):
    postID = models.ForeignKey(Post, on_delete=models.CASCADE)
    authorID = models.ForeignKey('author.Author', on_delete=models.CASCADE)
    date = models.DateTimeField()
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['postID', 'authorID'], name='Unique Like')
        ]
    
    def get_date(self):
        return self.date


class Comment(models.Model):
    commentID = models.CharField(max_length=32, primary_key=True)
    postID = models.ForeignKey(Post, on_delete=models.CASCADE)
    authorID = models.ForeignKey('author.Author', on_delete=models.CASCADE)
    date = models.DateTimeField()
    content = models.TextField()
    contentType = models.CharField(max_length=16)
