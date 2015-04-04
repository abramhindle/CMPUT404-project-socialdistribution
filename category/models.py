from django.db import models
from author.models import Author,FriendRequest
from images.models import Image
from author.models import Author
from post.models import Post


class Category(models.Model):
    name = models.CharField(max_length=128,unique=True)
    
    def __unicode__(self):
        return self.name
    
class PostCategory(models.Model):
    post = models.ForeignKey(Post)
    categories = models.ManyToManyField(Category)

    def __unicode__(self):
        return "id: %s" % (self.id)

    @staticmethod
    def getCategoryForPost(post):
        try:
            categorizedPost = PostCategory.objects.get(post=post)
        except PostCategory.DoesNotExist:
            return None

        return categorizedPost.categories.all()

    @staticmethod
    def addCategoryToPost(post, category_name):
        categorizedPost,_ = PostCategory.objects.get_or_create(post=post)
        category,_ = Category.objects.get_or_create(name=category_name)

        if (category not in categorizedPost.categories.all()):
            categorizedPost.categories.add(category)
        else:
            raise Exception()

    @staticmethod
    def getPostWithCategory(category_name):
        return PostCategory.objects.filter(categories__name=category_name).distinct()

    @staticmethod
    def removeCategory(post, category):
        try:
            categorizedPost = PostCategory.objects.get(post=post)
            category = Category.objects.get(name=category)
            categorizedPost.categories.remove(category)
        except:
            return None
