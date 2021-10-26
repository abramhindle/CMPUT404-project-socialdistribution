from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
import uuid

class Author(models.Model):
    type = models.CharField(default='author', max_length=100)
    uuid = models.UUIDField(primary_key=True, null=False, default=uuid.uuid4, editable=False)
    id = models.URLField(null=True)
    url = models.URLField(null=True)
    host = models.URLField(null=True)
    displayName = models.CharField(null=True, max_length=100)
    github = models.URLField(null=True)
    profileImage = models.URLField(null=True)
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    # symmetrical=False allows Author to follow people that don't follow them
    followers = models.ManyToManyField("self", symmetrical=False, blank=True)

    def __init__(self, *args, **kwargs):
        super(Author, self).__init__(*args, **kwargs)
        if self.host != None:
            # make sure host ends with a '/'
            self.host += '/' if (not self.host.endswith('/')) else ''

            # set id and url to format specified in the project specifications
            self.id = self.host + self.type + '/' + str(self.uuid)
            self.url = self.id


# https://stackoverflow.com/a/52196396 to auto-create Author when User is created
# @receiver(post_save, sender=User)
# def create_user_author(sender, instance, created, **kwargs):
#     if created:
#         Author.objects.create(user=instance)
#     instance.author.save()


class FriendRequest(models.Model):
    type = models.CharField(default='follow', max_length=100)
    summary = models.CharField(null=True, max_length=500)
    actor = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='actor')
    object = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='object')



class Post(models.Model):
    type = models.CharField(default='post', max_length=50)
    id = models.CharField(primary_key=True, max_length=50)
    title = models.CharField(max_length=200)
    description = models.CharField(null=True,blank=True,max_length=300)
    origin = models.CharField(max_length=200)
    visibility = models.CharField(default='public', max_length=20)
    author = models.ForeignKey(Author,on_delete=models.CASCADE)

class Comment(models.Model):
    type = models.CharField(default='comment', max_length=50)
    author = models.ForeignKey(Author,on_delete=models.CASCADE)
    post = models.ForeignKey(Post,on_delete=models.CASCADE)
    comment = models.CharField(max_length=300)
    published = models.DateTimeField(auto_now_add=True)
    id = models.CharField(primary_key=True, max_length=400)

# class Like(models.Model):
#     author = models.CharField(default='0',max_length=100)
#     postID = models.CharField(null=True, blank=True, max_length=100)
#     commentID = models.CharField(null=True, blank=True, max_length=100)
