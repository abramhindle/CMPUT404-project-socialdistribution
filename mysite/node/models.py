from django.db import models
import uuid
# Create your models here.
class Node(models.Model):

    NODESTATUS = (("U", "Unprocessed"), ("A", "Accepted"))
    host = models.URLField(primary_key=True)
    date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length = 1,choices=NODESTATUS, default="U")

    def __str__(self):
        return f"{self.host} {self.status}"
