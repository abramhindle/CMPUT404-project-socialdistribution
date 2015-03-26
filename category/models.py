from django.db import models
from author.models import Author,FriendRequest
from images.models import Image
from author.models import Author

from post.templatetags.post_extra import datesince
from post.models import Post
# Create your models here.

class Category(models.Model):
    name=models.CharField(max_length=128,unique=True)
    
    def __unicode__(self):
        return self.name
    
class PostCategory(models.Model):

    categories=models.ManyToManyField(Category)
    PRIVATE = 'private'
    ANOTHER_AUTHOR = 'author'
    FRIENDS = 'friends'  # make need to pluralize it => potential db migrations
    FOAF = 'foaf'
    SERVERONLY = 'severOnly'
    PUBLIC = 'public'

    PLAIN_TEXT = 'text/plain'
    MARK_DOWN = 'text/x-markdown'

    guid = models.CharField(max_length=64, unique=True)
    title = models.CharField(max_length=128)
    description = models.CharField(max_length=512)
    content = models.TextField()
    visibility = models.CharField(max_length=20,
                                  default=PUBLIC)

    content_type = models.CharField(max_length=100,
                                    default=PLAIN_TEXT)

    publication_date = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(Author)


    def __unicode__(self):
        return "id: %s\ntext: %s" % (self.id, self.content)
    # TODO stringfy all of the values
    def getJsonObj(self):
        jsonData = {}
        jsonData['title'] = str(self.title)
        jsonData['categories'] = str(self.categories)
        jsonData['description'] = str(self.description)
        jsonData['content-type'] = str(self.content_type)
        jsonData['content_type'] = str(self.content_type)
        jsonData['content'] = str(self.content)
        url = str(self.author.host + "author/posts/" + self.guid)
        jsonData['source'] = url
        jsonData['origin'] = url

        authorJson = {}
        authorJson['id'] = str(self.author.uuid)
        authorJson['host'] = str(self.author.host)
        authorJson['displayName'] = str(self.author.user.username)
        authorJson['url'] = str(self.author.host + "author/" + self.author.uuid)

        jsonData['author'] = authorJson
        jsonData['guid'] = str(self.guid)
        jsonData['pubDate'] = str(self.publication_date.strftime("%a %b %d %H:%M:%S %Z %Y"))
        jsonData['visibility'] = str(self.visibility).upper()


        return jsonData

    @staticmethod
    def getCategoryForPost(post):
        return Category.objects.filter(post=post)
    @staticmethod
    def removeCatagory(category_id):
        Category.objects.filter(guid=category_id).delete()