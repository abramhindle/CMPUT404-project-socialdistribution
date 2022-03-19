from django.db import models
import uuid
from posts.models import Post
from authors.models import Author


#  {
#      "@context": "https://www.w3.org/ns/activitystreams",
#      "summary": "Lara Croft Likes your post",         
#      "type": "Like",
#      "author":{
#          "type":"author",
#          "id":"http://127.0.0.1:5454/authors/9de17f29c12e8f97bcbbd34cc908f1baba40658e",
#          "host":"http://127.0.0.1:5454/",
#          "displayName":"Lara Croft",
#          "url":"http://127.0.0.1:5454/authors/9de17f29c12e8f97bcbbd34cc908f1baba40658e",
#          "github":"http://github.com/laracroft",
#          "profileImage": "https://i.imgur.com/k7XVwpB.jpeg"
#      },
#      "object":"http://127.0.0.1:5454/authors/9de17f29c12e8f97bcbbd34cc908f1baba40658e/posts/764efa883dda1e11db47671c4a3bbd9e"
# }
  

class Likes(models.Model):


    type = models.CharField(max_length=100, default="Like")
    author_url = models.URLField(max_length=250)
    summary = models.TextField(blank=False)
    context = models.URLField(blank=False)
    object= models.URLField(max_length=250, blank=False)
    # post = models.ForeignKey(Post,on_delete=models.CASCADE,default='')
