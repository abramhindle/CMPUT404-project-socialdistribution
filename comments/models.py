from django.db import models

MAX_LENGTH = 100
SMALLER_MAX_LENGTH = 50


# Create your models here.
class Comments(models.Model):
    type = models.CharField(max_length=SMALLER_MAX_LENGTH)
    page =  models.IntegerField()
    size = models.IntegerField()
    post = models.URLField(max_length=MAX_LENGTH)
    comment_id = models.URLField(max_length=MAX_LENGTH)

class Comment(models.Model):
    type = models.CharField(max_length=SMALLER_MAX_LENGTH)
 #   comment_author =  models.OneToOneField(Author, on_delete=models.CASCADE) # title of a post
    comment_content = models.TextField(max_length=MAX_LENGTH)
    content_type = models.CharField(max_length=SMALLER_MAX_LENGTH)
    pub_date = models.DateTimeField()
    comment_id = models.URLField(max_length=MAX_LENGTH)
   # comment = models.ForeignKey(Comments, on_delete=models.CASCADE) (brings up an error when running server)
