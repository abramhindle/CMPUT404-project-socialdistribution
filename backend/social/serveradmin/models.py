from django.db import models

# Create your models here.
class Image(models.Model):
    name = models.AutoField(primary_key=True)
    uploaded_img = models.ImageField(upload_to='images/')

