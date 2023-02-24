from django.db import models
from author.models import Author

# Create your models here.
class Post(models.Model):
    id = models.AutoField(primary_key=True, editable=False)
    url = models.URLField(editable=False)
    author = models.ForeignKey(Author, related_name="posts", on_delete=models.CASCADE)

    title = models.CharField(max_length=100)
    description = models.CharField(blank=True, default="", max_length=500)

    PUBLIC = 'false'
    PRIVATE = 'true'
    
    privacy_choices = [
        (PUBLIC, 'Public'),
        (PRIVATE, 'Private'),
    ]

    private = models.CharField(choices=privacy_choices, default="false", max_length=20)

    MARKDOWN = 'text/markdown'
    PLAIN = 'text/plain'
    IMAGE = 'image'
    
    content_types = [
        (MARKDOWN, 'markdown'),
        (PLAIN, 'plain'),
        (IMAGE, 'image')
    ]

    content_type = models.CharField(choices=content_types, default=PLAIN, max_length=20)
    
    # you may need to pip install pillow
    uploaded_img = models.ImageField(null=True, blank=True, upload_to='images/')

class Comments(models.Model):
    id = models.AutoField(primary_key=True, editable=False)
    url = models.URLField(editable=False)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    comment = models.TextField(max_length=200)
    