from django.db import models

MAX_LENGTH = 100
SMALLER_MAX_LENGTH = 50


# Create your models here.
'''
{
"type": "followers",
"items": [ {"type":"author",...}, ...]
}
'''
class Followers(models.Model):
    type = models.CharField(max_length=SMALLER_MAX_LENGTH)



class Follow(models.Model):
    type = models.CharField(max_length=SMALLER_MAX_LENGTH)
    # put in summary here
   # actor = models.ForeignKey(Author, on_delete=models.CASCADE)
   # object = models.ForeignKey(Author, on_delete=models.CASCADE)
