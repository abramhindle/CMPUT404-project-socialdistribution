from django.db import models
from mysite.user.models import User
import uuid

# Create your models here.
class Friend(models.Model):
    class Meta:
        unique_together = (("f1Id", "f2Id"),)

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    FRIENDSTATUS = (("U", "Unprocessed"), ("A", "Accepted"))
    date = models.DateField(auto_now_add=True)
    f1Id = models.ForeignKey(User, on_delete=models.CASCADE, related_name="f1Ids",to_field="username")
    f2Id = models.ForeignKey(User, on_delete=models.CASCADE, related_name="f2Ids",to_field="username")
    status = models.CharField(max_length=1, choices=FRIENDSTATUS, default="U")

    def __str__(self):
        return self.status
