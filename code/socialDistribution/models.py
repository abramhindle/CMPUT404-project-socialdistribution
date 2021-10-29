from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import User
from datetime import *
import timeago

from cmput404.constants import HOST, API_PREFIX


class Author(models.Model):
    '''
    Author model:
        user                Author's corresponding Django User (text)
        username            Author's username (text)
        displayName         Author's displayName (text)
        githubUrl           Author's github url (text)
        profileImageUrl     Author's profile image url (text)
        followers           Author's followers (array)
    '''
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    username = models.CharField(max_length=50, default='', unique=True)
    displayName = models.CharField(max_length=50)
    githubUrl = models.CharField(max_length=50, null=True)
    profileImageUrl = models.CharField(max_length=50, null=True)
    followers = models.ManyToManyField('Author', blank=True)

    def has_follower(self, author):
        return self.followers.filter(pk=author.id).exists()

    def is_friends_with(self, author):
        return self.followers.filter(pk=author.id).exists() and \
            author.followers.filter(pk=self.id).exists()

    def get_visible_posts_to(self, author):
        visible_posts = None
        if author.id == self.id:
            visible_posts = Post.objects.filter(author__pk=author.id)
        elif self.is_friends_with(author):
            visible_posts = Post.objects.filter(author__pk=self.id).exclude(visibility=Post.PRIVATE)
        else:
            visible_posts = Post.objects.filter(author__pk=self.id, visibility=Post.PUBLIC)

        return visible_posts.order_by('-pub_date')[:]

    def __str__(self):
        return self.displayName

    def as_json(self):
        return {
            "type": "author",
            # ID of the Author
            "id": f"http://{HOST}/{API_PREFIX}/author/{self.id}",
            # the home host of the author
            "host": f'http://{HOST}/{API_PREFIX}/',
            # the display name of the author
            "displayName": self.displayName,
            # url to the authors profile
            "url": f"http://{HOST}/{API_PREFIX}/author/{self.id}",
            # HATEOS url for Github API
            "github": self.githubUrl,
            # Image from a public domain
            # #TODO
            "profileImage": self.profileImageUrl
        }


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

    def as_json(self):
        return {
            "type": "comment",
            "author": self.author.as_json(),
            "comment": self.comment,
            "contentType": "text/markdown",
            "published": str(self.pub_date),
            "id": f"http://{HOST}/{API_PREFIX}/author/{self.post.author.id}/posts/{self.post.id}/comments/{self.id}",
        }


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

    TITLE_MAXLEN = 50
    DESCRIPTION_MAXLEN = 50
    CONTEXT_TEXT_MAXLEN = 200
    CONTENT_MEDIA_MAXLEN = 1000
    URL_MAXLEN = 2048

    title = models.CharField(max_length=TITLE_MAXLEN)
    source = models.URLField(max_length=URL_MAXLEN)
    origin = models.URLField(max_length=URL_MAXLEN)
    description = models.CharField(max_length=DESCRIPTION_MAXLEN)

    content_type = models.CharField(
        choices=PostContentType.choices,
        max_length=4,
        default=PostContentType.PLAIN
    )

    content_text = models.TextField(max_length=CONTEXT_TEXT_MAXLEN)

    # Base64 encoded binary field (image/png, image/jpg, application/base64)
    content_media = models.BinaryField(
        max_length=CONTENT_MEDIA_MAXLEN, null=True, blank=True)
    author = models.ForeignKey('Author', on_delete=models.CASCADE)

    count = models.PositiveSmallIntegerField(default=0)
    pub_date = models.DateTimeField()

    PUBLIC = "PB"
    FRIENDS = "FRD"
    PRIVATE = "PR"
    VISIBILITY_CHOICES = (
        (PUBLIC, 'PUBLIC'),
        (FRIENDS, 'FRIENDS'),
        (PRIVATE, 'PRIVATE')
    )

    visibility = models.CharField(
        max_length=10, choices=VISIBILITY_CHOICES, default=PUBLIC)
    unlisted = models.BooleanField()
    likes = models.ManyToManyField(
        'Author', related_name="liked_post", blank=True)

    @classmethod
    def get_all_friends_posts(cls, author):
        '''
        Get the posts created by friends of author
        '''
        followed_author_set = Author.objects.filter(followers__id=author.id)
        follower_author_set = author.followers.all()
        friends_set = followed_author_set and follower_author_set   # friends set
        return cls.objects.filter(
            unlisted=False,
            author__in=friends_set, 
            visibility=Post.FRIENDS,
        )

    @classmethod
    def get_latest_posts(cls, author):
        '''
        Get the author's posts and all the posts created by
        author's friends
        '''
        # public posts not created by user
        public_posts_set = cls.objects.filter(
            unlisted=False, 
            visibility=Post.PUBLIC
        ).exclude(author=author)

        # all listed posts created by user
        user_posts_set = cls.objects.filter(
            unlisted=False,
            author=author
        )

        friends_posts_set = cls.get_all_friends_posts(author)
        return public_posts_set.union(
            friends_posts_set,
            user_posts_set
        ).order_by("-pub_date")[:]

    def get_comments_as_json(self):
        author_id = self.author.id
        comments_set = Comment.objects.filter(
            post=self.id).order_by('-pub_date')[:5]
        comment_list = [comment.as_json() for comment in comments_set]
        return {
            "type": "comments",
            "page": 1,
            "size": 5,
            "post": f"http://{HOST}/{API_PREFIX}/author/{author_id}/posts/{self.id}",
            "id": f"http://{HOST}/{API_PREFIX}/author/{author_id}/posts/{self.id}/comments",
            "comments": comment_list
        }

    def has_media(self):
        '''
        Check if post has an attached image
        '''
        return self.content_type in [
            self.PostContentType.PNG,
            self.PostContentType.JPEG,
            self.PostContentType.BASE64
        ]

    def is_public(self):
        '''
        Check if post is public
        '''
        return self.visibility == self.PUBLIC

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
    
    def as_json(self):
        previousCategories = Category.objects.filter(post=self)
        previousCategoriesNames = [cat.category for cat in previousCategories]
        return {
            "type":"post",
            # title of a post
            "title":self.title,
            # id of the post
            "id": f"http://{HOST}/{API_PREFIX}/author/{self.author.id}/posts/{self.id}",
            # where did you get this post from?
            "source":self.source,
            # where is it actually from
            "origin":self.origin,
            # a brief description of the post
            "description":self.description,
            # The content type of the post
            # assume either
            # text/markdown -- common mark
            # text/plain -- UTF-8
            # application/base64
            # image/png;base64 # this is an embedded png -- images are POSTS. So you might have a user make 2 posts if a post includes an image!
            # image/jpeg;base64 # this is an embedded jpeg
            # for HTML you will want to strip tags before displaying
            "contentType":self.content_type,
            "content":self.content_text, # 
            # the author has an ID where by authors can be disambiguated
            "author":self.author.as_json(),
            # categories this post fits into (a list of strings
            "categories":previousCategoriesNames,
            # comments about the post
            # return a maximum number of comments
            # total number of comments for this post
            "count": self.count,
            # the first page of comments
            "comments":f"http://{HOST}/{API_PREFIX}/author/{self.author.id}/posts/{self.id}/comments/",
            # commentsSrc is OPTIONAL and can be missing
            # You should return ~ 5 comments per post.
            # should be sorted newest(first) to oldest(last)
            # this is to reduce API call counts
            "commentsSrc":self.get_comments_as_json(),
            # ISO 8601 TIMESTAMP
            "published":str(self.pub_date),
            # visibility ["PUBLIC","FRIENDS"]
            "visibility":self.visibility,
            # for visibility PUBLIC means it is open to the wild web
            # FRIENDS means if we're direct friends I can see the post
            # FRIENDS should've already been sent the post so they don't need this
            "unlisted":self.unlisted
            # unlisted means it is public if you know the post name -- use this for images, it's so images don't show up in timelines
        }

class Inbox(models.Model):
    '''
    Inbox model:
        author          author associated with the inbox (primary key)
        posts           posts pushed to this inbox (M2M)
        followRequests  follow requests pushed to this inbox (M2M)
    '''
    author = models.OneToOneField(
        'Author', on_delete=models.CASCADE, primary_key=True)
    posts = models.ManyToManyField(
        'Post', related_name='pushed_posts', blank=True)
    follow_requests = models.ManyToManyField(
        'Author', related_name='follow_requests', blank=True)

    def has_req_from(self, author):
        return self.follow_requests.filter(pk=author.id).exists()

    def add_post(self, post):
        try:
            self.posts.add(post)
        except ValidationError:
            raise