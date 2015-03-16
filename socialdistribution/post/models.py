from django.db import models
from author.models import Author, FriendRequest
from images.models import Image

import markdown


class Post(models.Model):
    """
    Post class represents the posts made by the authors
    Each post is associated with one author
    """

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

    # returns a json object of the current post object
    def getJsonObj(self):
        jsonData = {}
        jsonData['title'] = self.title
        jsonData['description'] = self.description
        jsonData['content-type'] = self.content_type

        authorJson = {}
        authorJson['id'] = self.author.uuid  # TODO: this needs to be valid
        authorJson['host'] = self.author.host
        authorJson['displayName'] = self.author.user.username  # TODO: this needs to be display name
        authorJson['url'] = 120  # TODO: get the url here

        #todo move the comment json objs into views
        # comments = []
        # commentList = comment.Comment.objects.filter(post=self)
        # for comment in commentList:
        #     comments.append(comment.getJsonObj())

        jsonData['author'] = authorJson
        jsonData['guid'] = self.guid
        jsonData['pubDate'] = self.publication_date #TODO needs to be processed
        jsonData['visibility'] = str(self.visibility).upper()
        # jsonData['comments'] = comments

        return jsonData

    @staticmethod
    def deletePost(postId):
        Post.objects.filter(guid=postId).delete()

    @staticmethod
    def getVisibilityTypes():
        visFriendlyString = {
            'private': 'Private',
            'author': 'Another Author',
            'friends': 'Friends',
            'foaf': 'Friends of Friends',
            'serverOnly': 'Server Only',
            }
        return visFriendlyString

    # Checks whether or not the viewer is able to see the post passed in
    def isViewable(self, viewer, author):

        visibility = self.visibility

        if visibility == Post.PRIVATE:
            return viewer == author
        elif visibility == Post.ANOTHER_AUTHOR:
            post_entry = VisibleToAuthor.objects.filter(visibleAuthor=viewer, post=self)
            # todo: get the entry from another server as well
            return post_entry.exists() or viewer == author
        elif visibility == Post.FRIENDS:
            return FriendRequest.is_friend(viewer, author) or viewer == author
        elif visibility == Post.FOAF:
            friendOfFriends = []
            friends = FriendRequest.get_friends(author)
            for friend in friends:
                friendOfFriends += FriendRequest.get_friends(friend)
            return viewer in friendOfFriends or viewer == author
        elif visibility == Post.SERVERONLY:
            # return viewer.isLocal() or viewer == author
            return True
        else:
            # Assuming that the visibility type is public
            return True

    @staticmethod
    def getVisibleToAuthor(viewer, author=None):
        resultList = []
        if author == None:
            postList = Post.objects.all()
        else:
            postList = Post.objects.filter(author=author)

        for post in postList:
            if post.isViewable(viewer, post.author):
                if post.content_type == Post.MARK_DOWN:
                    post.content = markdown.markdown(post.content)
                resultList.append(post)

        return resultList

    @staticmethod
    def getByAuthor(author):
        return Post.objects.filter(author=author)


class VisibleToAuthor(models.Model):

    """
    Data model relationship between an author and post where author is the person
    that the post was specifically created for
    """

    post = models.ForeignKey(Post)
    visibleAuthor = models.ForeignKey(Author)

    def __unicode__(self):
        return "specific post %s visible to only %s" % (self.post.id, self.visibleAuthor.user)


class PostImage(models.Model):

    """
    Data model relationship for post and images related to the post
    """

    post = models.ForeignKey(Post)
    image = models.ForeignKey(Image)

    def __unicode__(self):
        return "post %s has image %s" % (self.post.id, self.image.id)