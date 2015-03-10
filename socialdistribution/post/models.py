import datetime
from django.db import models
from author.models import Author
from images.models import Image
from django.db.models import Q



class Post(models.Model):

    PRIVATE = 'private'
    ANOTHER_AUTHOR = 'author'
    FRIENDS = 'friend' # make need to pluralize it => potential db migrations
    FOAF = 'friendsOfFriends'
    SERVERONLY = 'friendsOwnHost'
    PUBLIC = 'public'

    visFriendlyString = {
        PRIVATE: 'Private',
        ANOTHER_AUTHOR: 'Another Author',
        FRIENDS: 'Friends',
        FOAF: 'Friends of Friends',
        SERVERONLY: 'Server Only',
    }

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

    def getJsonObj(self):
        jsonData = {}
        jsonData['title'] = self.post.title
        jsonData['description'] = self.post.description
        jsonData['content-type'] = self.post.content_type

        authorJson = {}
        authorJson['id'] = self.author.id # TODO: this needs to be valid
        authorJson['host'] = self.author.host
        authorJson['displayName'] = self.author.name #TODO: this needs to be display name
        authorJson['url'] = 120 #TODO: get the url here

        jsonData['author'] = authorJson
        jsonData['guid'] = self.post.guid
        jsonData['pubDate'] = self.post.publication_date
        jsonData['visibility'] = self.post.visibility

        #TODO: still need comments in the json data
        return jsonData

    @staticmethod
    def deletePost(postId):
        # this should delete the entries in the relational table as well according to the docs
        Post.objects.filter(id=postId).delete()

    def getVisibilityTypes(self):
        return self.visFriendlyString

    # Checks whether or not the viewer is able to see the post passed in
    def isViewable(self, viewer, author):

        visibility = self.visibility

        if visibility == Post.PRIVATE:
            return viewer == author
        elif visibility == Post.ANOTHER_AUTHOR:
            post_entry = VisibleToAuthor.objects.filter(visibleAuthor=author, post=self)
            # todo: get the entry from another server as well
            return post_entry.exists()
        elif visibility == Post.FRIENDS:
            return Author.get_status(viewer, author)
        elif visibility == Post.FOAF:
            return (viewer in Author.get_friends(author))
        elif visibility == Post.SERVERONLY:
            return viewer.isLocal()
        else:
            # Assuming that the visibility type is public
            return True

    @staticmethod
    def getVisibleToAuthor(author):
        resultList = []
        postByEveryone = Post.objects.all()

        #TODO: Need to get the items other servers

        for post in postByEveryone:
            if post.isViewable(author, post.author):
                resultList.append(post)

        return resultList


    @staticmethod
    def getByAuthor(author):
        return Post.objects.filter(author=author)

#TODO: remove this and add author to foreignkey in post
# class AuthoredPost(models.Model):
#     author = models.ForeignKey(Author)
#     post = models.ForeignKey(Post)
#
#     def __unicode__(self):
#         return "post %s made by %s" % (self.author.user, self.post.id)
#
#     def getJsonObj(self):
#         jsonData = {}
#         jsonData['title'] = self.post.title
#         jsonData['description'] = self.post.description
#         jsonData['content-type'] = self.post.content_type
#
#         authorJson = {}
#         authorJson['id'] = self.author.id # TODO: this needs to be valid
#         authorJson['host'] = self.author.host
#         authorJson['displayName'] = self.author.name #TODO: this needs to be display name
#         authorJson['url'] = 120 #TODO: get the url here
#
#         jsonData['author'] = authorJson
#         jsonData['guid'] = self.post.guid
#         jsonData['pubDate'] = self.post.publication_date
#         jsonData['visibility'] = self.post.visibility
#
#         #TODO: still need comments in the json data
#         return jsonData



class VisibleToAuthor(models.Model):
    post = models.ForeignKey(Post)
    visibleAuthor = models.ForeignKey(Author)

    def __unicode__(self):
        return "specific post %s visible to only %s" % (self.post.id, self.visibleAuthor.user)

class PostImage(models.Model):
    post = models.ForeignKey(Post)
    image = models.ForeignKey(Image)

    def __unicode__(self):
        return "post %s has image %s" % (self.post.id, self.image.id)