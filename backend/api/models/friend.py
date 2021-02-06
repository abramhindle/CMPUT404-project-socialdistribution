from django.db import models
import uuid

# Related Model
from api.models.author import Author


# NOTE: When a friend record is created there should be two records made, with each user as the primary friend
class Friend(models.Model):
    # The author whose is primary in this relationship
    author_id = models.ForeignKey(Author, null=False, on_delete=models.CASCADE, related_name="my_author_id")

    # The friend of this author
    my_friends_id = models.ForeignKey(Author, null=False, on_delete=models.CASCADE, related_name="my_friends_id")

    # Note Sure how this will work yet, please look into it when you work on friends
    url= models.URLField(null=True)

    published = models.DateField(auto_now_add=True)

    # Do we wanna know when someone was un-befriended? Or is it enough to simply delete a friend record?
