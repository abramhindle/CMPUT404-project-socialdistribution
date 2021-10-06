# from django.db import models
# # An abstract base class implementing a fully featured User model with admin-compliant permissions.
# #Username and password are required. Other fields are optional.
# from django.contrib.auth.models import AbstractUser
# from django.conf import settings


# # Create our models here.
# class Author(AbstractUser):
#     type = models.CharField(max_length=200, default='Author')
#     user = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True)
#     timestamp = models.DateTimeField(auto_now_add= True, auto_now= False, blank = True)

#     def __str__(self):
#         return self.task

from django.db import models
from django.contrib.auth.models import User

class Author(models.Model):
    task = models.CharField(max_length = 180,default='SOME STRING')
    timestamp = models.DateTimeField(auto_now_add = True, auto_now = False, blank = True)
    completed = models.BooleanField(default = False, blank = True)
    updated = models.DateTimeField(auto_now = True, blank = True)
    user = models.ForeignKey(User, on_delete = models.CASCADE, blank = True, null = True)

    def __str__(self):
        return self.task