from django.db import models
from django.db.models import Q
from author.models import Author, FriendRequest
from images.models import Image
from author.models import Author
from post.models import Post


class Category(models.Model):
    name = models.CharField(max_length=128, unique=True)

    def __unicode__(self):
        return self.name


class PostCategory(models.Model):
    post = models.ForeignKey(Post)
    categories = models.ManyToManyField(Category)

    def __unicode__(self):
        return "id: %s\ntext: %s" % (self.id, self.content)

    @staticmethod
    def getCategoryForPost(post):
        return PostCategory.objects.filter(post=post)

    @staticmethod
    def removeCategory(post, category):
        try:
            categorizedPost = PostCategory.objects.get(post=post)
            category = Category.objects.get(name=category)
            categorizedPost.entry_set.remove(category)
        except:
            return None
