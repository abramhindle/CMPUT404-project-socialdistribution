from django.db import models
from django.contrib.auth.models import User
from datetime import *
import timeago

# Create your models here.

## DUMMY
class Author(models.Model):
    '''
    Author model:
        user                Author's corresponding Django User (text)
        username            Author's username (text)
        displayName         Author's displayName (text)
        githubUrl           Author's github url (text)
    '''
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    username = models.CharField(max_length=50, default='', unique=True)
    displayName = models.CharField(max_length=50)
    githubUrl = models.CharField(max_length=50, null=True)
    followers = models.ManyToManyField('Author', blank=True)

    def has_follower(self, author):
        return self.followers.filter(pk=author.id).exists()

    def is_friends_with(self, author):
        return self.followers.filter(pk=author.id).exists() and \
            author.followers.filter(pk=self.id).exists()

    def __str__(self):
        return self.displayName


class Comment(models.Model):
    '''
    Comment model:
        author              Comment author (reference to author)
        content_type        Markdown or Text
        comment             Comment content (markdown or text)
        pub_date            Published date (datetime)
        post                Post related to the comment (reference to post)
        id                  Auto-generated id
    '''
    class CommentContentType(models.TextChoices):
        PLAIN = 'PL', 'text/plain'
        MARKDOWN = 'MD', 'text/markdown'

    author = models.ForeignKey('Author', on_delete=models.CASCADE)
    content_type = models.CharField(
        max_length=2,
        choices=CommentContentType.choices
    )
    comment = models.CharField(max_length=200)

    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    pub_date = models.DateTimeField()

    def when(self):
        '''
        Returns string describing when the comment was created
        '''
        now = datetime.now(timezone.utc)
        return timeago.format(self.pub_date, now)


class Category(models.Model):
    '''
    Categories model:
        id                  Auto-generated id
        category            Category name
        post                reference to post (Many-to-One relationship)
    '''
    category = models.CharField(max_length=50)
    post = models.ForeignKey('Post', on_delete=models.CASCADE)


class Post(models.Model):
    '''
    Post model:
        title               Post title (a Text)
        id (default)        Auto-generated id

        source              Where the post was obtained (a URL)
        origin              original source (a URL)
        description         Post description (a Text)

        content_type        Type of post's content:
                                - markdown
                                - plain text (default)
                                - png
                                - jpeg
                                - base64 (binary data)

        content_text        Actual text-type content (markdown or plain text)
        content_media       Any attached images (base64 encoded image; png or jpeg)

        author              Post author (reference to author)
        
        count               total number of comments (small integer)
        page_size           page size  (small integer)
        first_comments_page URL of first comments page

        pub_date            Post published date (datetime)
        visibility          PUBLIC or FRIENDS
        unlisted            Boolean indicating whether post is listed or not
        likes               Authors that liked this post
        
    '''
    class PostContentType(models.TextChoices):
        MARKDOWN = 'MD', 'text/markdown'
        PLAIN = 'PL', 'text/plain'
        BASE64 = 'B64', 'application/base64'
        PNG = 'PNG', 'image/png;base64'
        JPEG = 'JPEG', 'image/jpeg;base64'

    class PostVisibility(models.TextChoices):
        PUBLIC = "PB", "PUBLIC"
        FRIENDS = "FRD", "FRIENDS"

    title = models.CharField(max_length=50)
    source = models.URLField(max_length=200)
    origin = models.URLField(max_length=200)
    description = models.CharField(max_length=50)

    content_type = models.CharField(
        choices=PostContentType.choices, 
        max_length=4,
        default=PostContentType.PLAIN
    )
    
    content_text = models.TextField()

    # Uploads to MEDIA ROOT uploads/ YEAR/ MONTH
    content_media = models.ImageField(upload_to="uploads/% Y/% m", null=True, blank=True)
    author = models.ForeignKey('Author', on_delete=models.CASCADE)

    count = models.PositiveSmallIntegerField(default=0)
    page_size = models.PositiveSmallIntegerField(default=0)
    first_comments_page = models.URLField(max_length=200, blank=True)
    pub_date = models.DateTimeField()

    visibility = models.CharField(max_length=10, choices=PostVisibility.choices)
    unlisted = models.BooleanField()
    likes = models.ManyToManyField('Author', related_name="liked_post", blank=True)

    def has_media(self):
        '''
        Check if post has an attached image
        '''
        return self.content_type in [
            self.PostContentType.PNG,
            self.PostContentType.JPEG
        ]

    def is_public(self):
        '''
        Check if post is public
        '''
        return self.visibility == self.PostVisibility.PUBLIC

    def when(self):
        '''
        Returns string describing when post the was created
        
        For example,
            3 days ago
            1 min ago
            5 secs ago
            etc
            ...
        '''
        now = datetime.now(timezone.utc)
        return timeago.format(self.pub_date, now)

    def total_likes(self):
        return self.likes.count()
        

class Inbox(models.Model):
    '''
    Inbox model:
        author          author associated with the inbox (primary key)
        posts           posts pushed to this inbox (M2M)
        followRequests  follow requests pushed to this inbox (M2M)
    '''
    author = models.OneToOneField('Author', on_delete=models.CASCADE, primary_key=True)
    posts = models.ManyToManyField('Post', related_name='pushed_posts', blank=True)
    follow_requests = models.ManyToManyField('Author', related_name='follow_requests', blank=True)

    def has_req_from(self, author):
        return self.follow_requests.filter(pk=author.id).exists()