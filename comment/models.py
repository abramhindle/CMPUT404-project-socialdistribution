from django.db import models
from author.models import Author
from post.models import Post
from post.templatetags.post_extra import datesince

# Create your models here.

class Comment(models.Model):
    guid = models.CharField(max_length=128, unique=True)
    author = models.ForeignKey(Author)
    comment = models.TextField()
    pubDate = models.DateTimeField(auto_now=True)
    post = models.ForeignKey(Post)

    def __unicode__(self):
        return "comment with id %s and comment is %s" % (self.guid, self.comment)

    # TODO stringfy all of the values
    def getJsonObj(self):
        authorJson = {}
        authorJson['id'] = str(self.author.uuid)
        authorJson['host'] = str(self.author.host)
        authorJson['displayName'] = str(self.author.user.username)

        commentJson = {}
        commentJson['author'] = authorJson
        commentJson['comment'] = str(self.comment)
        commentJson['pubDate'] = str(self.pubDate.strftime("%a %b %d %H:%M:%S %Z %Y"))
        #This is only used by us since its not possible to timesince with a string in django timeplate
        commentJson['timeSince'] = datesince(commentJson['pubDate'])
        commentJson['guid'] = str(self.guid)
        commentJson['postId'] = str(self.post.guid)

        return commentJson

    @staticmethod
    def getCommentsForPost(post):
        return Comment.objects.filter(post=post)

    @staticmethod
    def removeComment(comment_id):
        Comment.objects.filter(guid=comment_id).delete()