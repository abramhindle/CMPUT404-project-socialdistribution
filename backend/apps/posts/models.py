from django.db import models

# Create your models here.
from django.urls import reverse
from apps.authors.models import Author
# Create your models here.


class Post(models.Model):

    # Fields
    title = models.CharField(max_length=250, blank=True)
    source = models.CharField(max_length=50, blank=True)
    origin = models.CharField(max_length=50, blank=True)
    description = models.CharField(max_length=250, blank=True)
    contentType = models.CharField(max_length=20, blank=True)
    author_id = models.ForeignKey(Author, on_delete=models.CASCADE)

    def document_template():
        return {"friend_id": "[]"}
    category = models.JSONField(blank=True, default=document_template)
    comment_list = models.JSONField(
        blank=True, verbose_name='comment', default=document_template)
    friend_list = models.JSONField(blank=True, default=document_template)
    count = models.PositiveBigIntegerField(default=0)
    publish_date = models.DateField(auto_now_add=True)
    is_public = models.BooleanField()
    image = models.ImageField(blank=True)

    def get_like(self):
        return self.count

    def increment_like(self):
        self.count = self.count + 1

    def get_id(self):
        return self.id

    def get_root_comments(self):
        """The plan is to call a function from the comment class and then get it here."""
        pass


class Comment(models.Model):
    message: models.CharField(max_length=250)
    parent_post_id = models.ForeignKey(
        Post, on_delete=models.CASCADE, blank=True, null=True)
    parent_comment_id = models.BigIntegerField(blank=True, null=True)

    def get_comment_id(self):
        return self.id
