from django.db import models
from author.models import Author
import uuid
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.paginator import Paginator

class Post(models.Model):
    postID = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    ownerID = models.ForeignKey('author.Author', on_delete=models.CASCADE)
    date = models.DateTimeField()
    title = models.TextField()
    content = models.TextField()
    source = models.URLField(null=True)
    origin = models.URLField(null=True)
    description = models.TextField()
    # The categories field will be a semicolon separated set of tags
    categories = models.TextField()
    isPublic = models.BooleanField()
    isListed = models.BooleanField()
    hasImage = models.BooleanField()
    contentType = models.CharField(max_length=32)

    def get_url(self):
        return self.ownerID.get_url() + "/posts/" + str(self.postID)

    def get_categories(self):
        return self.categories.split(";")

    def get_comment_count(self):
        return Comment.objects.filter(postID=self.postID).count()

    def get_comment_url(self):
        return self.get_url() + "/comments"

    def get_comments(self):
        comments = Comment.objects.filter(postID=self.postID).order_by("-date")
        paginator = Paginator(comments, 5)
        return paginator.get_page(1)

    def get_visibility(self):
        if self.isPublic:
            return "PUBLIC"
        else:
            return "FRIENDS"

    def is_unlisted(self):
        if self.isListed:
            return False
        else:
            return True


class Like(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    objectID = models.CharField(max_length=200)
    content_object = GenericForeignKey('content_type', 'objectID')
    authorID = models.ForeignKey('author.Author', on_delete=models.CASCADE)
    summary = models.CharField(max_length=100)
    context = models.URLField(null=True, blank=True)
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['objectID', 'authorID'], name='Unique Like')
        ]

    def get_object_url(self):
        # return either comment url or post url depending on what object was liked
        if self.content_type.model == "post":
            post = Post.objects.get(postID = self.objectID)
            return post.get_url()
        else:
            comment = Comment.objects.get(commentID=self.objectID)
            return comment.get_id()


class Comment(models.Model):
    commentID = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    postID = models.ForeignKey(Post, on_delete=models.CASCADE)
    authorID = models.ForeignKey('author.Author', on_delete=models.CASCADE)
    date = models.DateTimeField()
    content = models.TextField()
    contentType = models.CharField(max_length=16)

    def get_id(self):
        return self.postID.get_url() + "/comments/" + str(self.commentID)

    def get_content(self):
        return self.content

    def get_date(self):
        return self.date

    def get_author(self):
        return self.authorID
