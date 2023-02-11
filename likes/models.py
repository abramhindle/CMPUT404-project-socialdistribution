from django.db import models
MAX_LENGTH = 100
SMALLER_MAX_LENGTH = 50

# Create your models here.
class Like(models.Model):
    context = models.URLField(max_length=MAX_LENGTH)
    # put in summary here
    type = models.CharField(max_length=SMALLER_MAX_LENGTH)
#    like_author =  models.OneToOneField(Author, on_delete=models.CASCADE) 
    content_type = models.CharField(max_length=SMALLER_MAX_LENGTH)
    object = models.URLField(max_length=MAX_LENGTH)
