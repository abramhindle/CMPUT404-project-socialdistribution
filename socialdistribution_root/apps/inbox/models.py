from django.db import models
from uuid import uuid4
from apps.core.models import Author

# Create your models here.
class InboxItem(models.Model):
    class ItemTypeEnum(models.TextChoices):
        POST = "post",
        FOLLOW = "follow",
        LIKE = "like"

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    author_id = models.ForeignKey(Author, on_delete=models.CASCADE) # guy who wrote the original post
    item_id = models.CharField(max_length=200) # This could be the id of an item that isn't in our databse so can't foreign key
    item_type = models.CharField(max_length=10, choices=ItemTypeEnum.choices)
    item = models.CharField(max_length=5000) # This is the content of the item