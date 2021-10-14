from django.db import models


class Post(models.Model):
    postID = models.CharField(max_length=32, primary_key=True)
    ownerID = models.ForeignKey('author.Author', on_delete=models.CASCADE)
    date = models.DateTimeField()
    content = models.TextField()
    isPublic = models.BooleanField()
    isListed = models.BooleanField()
    hasImage = models.BooleanField()
    contentType = models.CharField(max_length=16)
    host = models.URLField()

    def get_url(self):
        return self.host + "author/" + str(self.ownerID) + "/post/" + str(self.postID)


class Like(models.Model):
    postID = models.ForeignKey(Post, on_delete=models.CASCADE)
    authorID = models.ForeignKey('author.Author', on_delete=models.CASCADE)
    date = models.DateTimeField()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['postID', 'authorID'], name='Unique Like')
        ]


class Comment(models.Model):
    commentID = models.CharField(max_length=32, primary_key=True)
    postID = models.ForeignKey(Post, on_delete=models.CASCADE)
    authorID = models.ForeignKey('author.Author', on_delete=models.CASCADE)
    date = models.DateTimeField()
    content = models.TextField()
    contentType = models.CharField(max_length=16)
