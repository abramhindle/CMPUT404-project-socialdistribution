from django.db import models
from author.models import Author
from post.models import Post

# Create your models here.

class Comment(models.Model):

    guid = models.CharField(max_length=128, unique=True)
    author = models.ForeignKey(Author)
    comment = models.TextField()
    pubDate = models.DateTimeField(auto_now=True)
    post = models.ForeignKey(Post)

    def __unicode__(self):
        return "comment with id %s and comment is %s" % (self.guid, self.comment)

    def getJsonObj(self):
        authorJson = {}
        authorJson['id'] = self.author.uuid
        authorJson['host'] = self.author.host
        authorJson['displayName'] = self.author.user.username

        commentJson = {}
        commentJson['author'] = authorJson
        commentJson['comment'] = self.comment
        commentJson['pubDate'] = self.pubDate
        commentJson['guid'] = self.guid

        return authorJson

    @staticmethod
    def getCommentsForPost(post):
        return Comment.objects.filter(post=post)

    @staticmethod
    def removeComment(comment_id):
        Comment.objects.filter(guid=comment_id).delete()