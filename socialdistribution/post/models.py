import datetime
from django.db import models
from author.models import Author
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


    post_id = models.AutoField(primary_key=True)
    text = models.TextField()
    visibility = models.CharField(max_length=20,
                                  default=PUBLIC)

    mime_type = models.CharField(max_length=100,
                                 default=PLAIN_TEXT)

    publication_date = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)


    def __unicode__(self):
        return "id: %s\ntext: %s" % (self.post_id, self.text)

    @staticmethod
    def deletePost(postId):
        # this should delete the entries in the relational table as well according to the docs
        Post.objects.filter(post_id=postId).delete()

    def getVisibilityTypes(self):
        return self.visFriendlyString

    # Checks whether or not the viewer is able to see the post passed in
    @staticmethod
    def isViewable(post, viewer, author):

        visibility = post.visibility

        if visibility == Post.PRIVATE:
            return viewer == author
        elif visibility == Post.ANOTHER_AUTHOR:
            post_entry = VisibleToAuthor.objects.filter(visibleAuthor=author, post=post)
            # todo: get the entry from another server as well
            return post_entry.exists()
        elif visibility == Post.FRIENDS:
            return viewer.isFriend(author)
        elif visibility == Post.FOAF:
            return viewer.isFriendOfFriend(author)
        elif visibility == Post.SERVERONLY:
            return viewer.isLocal()
        else:
            # Assuming that the visibility type is public
            return True

    @staticmethod
    def getVisibleToAuthor(author):
        resultList = []
        postByAuthor = Post.getByAuthor(author)
        itemSet = VisibleToAuthor.objects.filter(visibleAuthor=author).select_related('post')
        visibleToAuthor = AuthoredPost.objects.filter(post=itemSet)
        postByEveryone = AuthoredPost.objects.filter(~Q(author=author))

        #TODO: Need to get the items other servers

        for authoredPost in postByEveryone:
            if (Post.isViewable(authoredPost.post, author, authoredPost.author)):
                resultList.append(authoredPost)

        for authoredPost in postByAuthor:
            if authoredPost not in resultList:
                resultList.append(authoredPost)

        for authoredPost in visibleToAuthor:
            if authoredPost not in resultList:
                resultList.append(authoredPost)

        return resultList


    @staticmethod
    def getByAuthor(author):
        return AuthoredPost.objects.filter(author=author)


class AuthoredPost(models.Model):
    author = models.ForeignKey(Author)
    post = models.ForeignKey(Post)

    def __unicode__(self):
        return "post %s made by %s" % (self.author.user, self.post.post_id)

class VisibleToAuthor(models.Model):
    post = models.ForeignKey(Post)
    visibleAuthor = models.ForeignKey(Author)

    def __unicode__(self):
        return "specific post %s visible to only %s" % (self.post.post_id, self.visibleAuthor.user)