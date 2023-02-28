from djongo import models
from service.models.author import Author
import uuid

class Followers(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name="all_authors")
    follower = models.ForeignKey(Author, on_delete=models.CASCADE, related_name="all_followers")
