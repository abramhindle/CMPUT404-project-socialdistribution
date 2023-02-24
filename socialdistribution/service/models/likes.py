from djongo import models
from service.models.author import Author
# Create your models here.

class Likes(models.Model):
    context = models.CharField()
    summary = models.CharField()
    type = "Like"
    author = models.OneToOneField(Author, on_delete=models.CASCADE)
    object = models.URLField()