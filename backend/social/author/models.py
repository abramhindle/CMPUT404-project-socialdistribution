from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Author(models.Model):
    id = models.AutoField(primary_key=True, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    friends = models.ManyToManyField('self')
    display_name = models.CharField(max_length=20, blank=False)
    profileImage = models.URLField(editable=True)
    url = models.URLField(editable=False)
    host = models.URLField(editable=False)
    