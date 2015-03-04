from django.db import models

from author.models import Author

# Create your models here.

class Post(models.Model):

    SELF = 'self'
    ANOTHER_AUTHOR = 'author'
    FRIENDS = 'friend'
    FRIENDS_OF_FRIENDS = 'friendsOfFriends'
    FRIENDS_OWN_HOST = 'friendsOwnHost'
    PUBLIC = 'public'

    PLAIN_TEXT = 'text/plain'
    MARK_DOWN = 'text/x-markdown'


    VISIBILITY_TYPE = (
        (SELF, 'Self'),
        (ANOTHER_AUTHOR, 'Another_Author'),
        (FRIENDS, 'Friends'),
        (FRIENDS_OF_FRIENDS, 'Friends_Of_Friends'),
        (FRIENDS_OWN_HOST, 'Friends_Own_Host'),
        (PUBLIC, 'Public'),
    )


    post_id = models.AutoField(primary_key=True);
    text = models.TextField()
    visibility = models.CharField(max_length=20,
                                  choices=VISIBILITY_TYPE,
                                  default=PUBLIC)

    mime_type = models.CharField(max_length=100,
                                 default=PLAIN_TEXT)

    publication_date = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)


    def __unicode__(self):
        return "id: %s\ntext: %s" % (self.post_id, self.text)

    def getByAuthor(self, author):
        posts = Post.objects.all()
        authored_posts = AuthoredPost.objects.filter('author__name'==author)

        post_list = []

        for post in posts:
            print 1

        return post_list


class AuthoredPost(models.Model):
    author = models.ForeignKey(Author)
    post = models.ForeignKey(Post)

    def __unicode__(self):
        return "post %s made by %s" % (self.author.id, self.post.post_id)

class PostVisibility(models.Model):
    author = models.ForeignKey(Author)
    post = models.ForeignKey(Post)

    def __unicode__(self):
        return "post %s is visible to %s" % (self.author.id, self.post.post_id)