from django.db import models

MAX_LENGTH = 100
SMALLER_MAX_LENGTH = 50

'''
{
"type": "authors",
"items": [ {"type":"author",...}, ...]
}
'''
class Authors(models.Model):
    type = models.CharField(max_length=SMALLER_MAX_LENGTH)
    


'''
{
"type": "author",
"id": ...
"host": ...
"displayName": ...
"url": ...
"github": ...
"profileImage": ...
}
'''
# Create your models here.
class Author(models.Model):
    type = models.CharField(max_length=SMALLER_MAX_LENGTH)
    author_id = models.URLField(max_length=MAX_LENGTH)  # ID of the author
    home_host = models.URLField() # the home host 
    display_name = models.CharField(max_length=MAX_LENGTH) # the display name
    profile_url = models.URLField() # url to the author's profile
    author_github = models.URLField(max_length=MAX_LENGTH) # HATEOS url for Github API
    profile_image = models.URLField(max_length=MAX_LENGTH) # Image from a public domain


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
    actor = models.ForeignKey(Author, on_delete=models.CASCADE)
    object = models.ForeignKey(Author, on_delete=models.CASCADE)


class Post(models.Model):
    type = models.CharField(max_length=SMALLER_MAX_LENGTH)
    title =  models.CharField(max_length=MAX_LENGTH) # title of a post
    post_id = models.URLField(max_length=MAX_LENGTH) # id of a post
    post_source = models.URLField(max_length=MAX_LENGTH) # where did you get this post from?
    post_origin =  models.URLField(max_length=MAX_LENGTH) # where is it actually from
    description = models.TextField(max_length=MAX_LENGTH) # a brief description of the post
    content_type = models.CharField(max_length=SMALLER_MAX_LENGTH)
    content = models.TextField(max_length=MAX_LENGTH)
    author = models.ForeignKey(Author, on_delete=models.CASCADE) # an author can write many posts
    # put in categories here
    comment_count = models.IntegerField()
    comments = models.URLField(max_length=MAX_LENGTH) 
    # commentsSrc is OPTIONAL and can be missing
    pub_date = models.DateTimeField()
    # put in visibility here
    is_unlisted = models.BooleanField()

class ImagePost(models.Model):
    pass

class Comments(models.Model):
    type = models.CharField(max_length=SMALLER_MAX_LENGTH)
    page =  models.IntegerField()
    size = models.IntegerField()
    post = models.URLField(max_length=MAX_LENGTH)
    comment_id = models.URLField(max_length=MAX_LENGTH)

class Comment(models.Model):
    type = models.CharField(max_length=SMALLER_MAX_LENGTH)
    comment_author =  models.OneToOneField(Author, on_delete=models.CASCADE) # title of a post
    comment_content = models.TextField(max_length=MAX_LENGTH)
    content_type = models.CharField(max_length=SMALLER_MAX_LENGTH)
    pub_date = models.DateTimeField()
    comment_id = models.URLField(max_length=MAX_LENGTH)
    comment = models.ForeignKey(Comments, on_delete=models.CASCADE) 

class Like(models.Model):
    context = models.URLField(max_length=MAX_LENGTH)
    # put in summary here
    type = models.CharField(max_length=SMALLER_MAX_LENGTH)
    like_author =  models.OneToOneField(Author, on_delete=models.CASCADE) 
    content_type = models.CharField(max_length=SMALLER_MAX_LENGTH)
    object = models.URLField(max_length=MAX_LENGTH)

    
class Liked(models.Model):
    context = models.URLField(max_length=MAX_LENGTH)
    # put in items here?

class Inbox(models.Model):
    type = models.CharField(max_length=SMALLER_MAX_LENGTH)
    author = models.URLField(max_length=MAX_LENGTH)
    # put in items (consists of posts) here?

    
    