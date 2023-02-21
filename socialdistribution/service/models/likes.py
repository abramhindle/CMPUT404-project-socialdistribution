from djongo import models
from author import Author
import uuid
from django.core import serializers

# Create your models here.

class Like(models.Model):
    context = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    summary = models.CharField()
    type = "Like"
    author = models.OneToOneField(Author, on_delete=models.CASCADE) #link an Author to a registered user
    object = author.id + "/posts/"