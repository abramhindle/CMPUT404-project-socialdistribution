from django.db import models

class Author(models.Model):
    display_name = models.CharField(max_length=200)
    profile_image = models.CharField(max_length=250)
    github_handle = models.CharField(max_length=200)

    def __str__(self):
        return self.display_name

class FollowRequest(models.Model):
    sender =  models.ForeignKey(Author, related_name='follow_requests_sent', on_delete=models.CASCADE)
    receiver =  models.ForeignKey(Author, related_name='follow_requests_received', on_delete=models.CASCADE) 

class Follow(models.Model):
    follower = models.ForeignKey(Author, related_name='following_authors', on_delete=models.CASCADE)
    followee = models.ForeignKey(Author, related_name='followed_by_authors', on_delete=models.CASCADE)
