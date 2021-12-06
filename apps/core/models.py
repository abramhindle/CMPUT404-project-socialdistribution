from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from uuid import uuid4


# Custom user class based on Django's provided AbstractUser.
# Allows modifying user if needed
class User(AbstractUser):
    """
    Users within the Django authentication system are represented by this
    model.

    Username and password are required. Other fields are optional.
    """
    class Meta(AbstractUser.Meta):
        swappable = 'AUTH_USER_MODEL'    

    @property
    def get_author(self):
        author = Author.objects.filter(userId=self).first()
        return author.id

# Create your models here.
class Author(models.Model):
    id = models.CharField(primary_key=True, max_length=200, default=uuid4, editable=False, unique=True)
    userId = models.ForeignKey(User, on_delete=models.CASCADE)
    displayName = models.CharField(('displayName'), max_length=80, blank=True)
    github = models.URLField(('github'), max_length=80, blank=True)
    profileImage = models.TextField(('profileImage'), default="", blank=True)
    isApproved = models.BooleanField(('isApproved'), default=False)
    isServer = models.BooleanField(default=False)

class Follow(models.Model):    
    # Note that db_constraint=False means there won't be a constraint requiring an author with this
    # id in our database. This is important for cases where the author is not in our database. 
    # If you try to access follower that doesn't exist you will get a Author.DoesNotExist error so you should use 
    # follower_id instead in that case.
    follower = models.ForeignKey(Author, db_column='follower', on_delete=models.CASCADE, db_constraint=False, related_name='follows') 
    target = models.ForeignKey(Author, db_column='target', on_delete=models.CASCADE, db_constraint=False, related_name='is_followed')

class ExternalHost(models.Model):
    # Must either have both username and password, or token. Can have all three

    host = models.CharField(('host'), max_length=80, blank=False)
    username = models.CharField(('username'), max_length=80, blank=True)
    password = models.CharField(('password'), max_length=80, blank=True)
    token = models.CharField(('token'), max_length=80, blank=True)

# The two settings we expect to use are "RequireApproval" and "AllowSignUp". These are auto added in the migration
# Other settings could be added in the future.
class Settings(models.Model):
    key = models.CharField(('key'), primary_key=True, max_length=80, blank=False, unique=True)
    value = models.CharField(('value'), max_length=80, blank=True)

@receiver(post_save, sender=User)
def my_handler(sender: User, **kwargs):
    if (kwargs['created']):
        user = kwargs['instance']
        Author.objects.create(userId=user, displayName=user.username)

######
# In the event that all migrations must be wiped, here is the migration file used to add the default settings. 
# This should be placed after whatever migration includes adding the Settings model itself to the database.
######
# def create_settings(apps, schema_editor):
#     Settings = apps.get_model("core", "Settings")
#     requireApproval = Settings.objects.create(key="RequireApproval",value="True")
#     requireApproval.save()

#     allowSignUp = Settings.objects.create(key="AllowSignUp",value="True")
#     allowSignUp.save()

# class Migration(migrations.Migration):

#     dependencies = [
#         ('core', '0010_settings'),
#     ]

#     operations = [
#         migrations.RunPython(create_settings)
#     ]

