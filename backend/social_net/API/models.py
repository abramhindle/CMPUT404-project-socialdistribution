from django.db import models

# Create your models here.

class AuthorModel(models.Model):
    type = models.CharField(max_length=100, blank=False, default='author')
    id = models.CharField(max_length=100, primary_key=True)
    url = models.CharField(max_length=100, default=id)
    host = models.CharField(max_length=100, blank=False, default='')
    displayName = models.CharField(max_length=100, blank=False, default='')
    github = models.CharField(max_length=100, blank=False, default='')
    profileImage = models.CharField(max_length=500, blank=False, default='')

    class Meta:
        ordering = ['type', 'id', 'host', 'displayName', 'profileImage']
        
        
# TODO: Put some effort into making sure these max_lengths make sense
class PostModel(models.Model):
    type = models.CharField(max_length=4, blank=False, default='post')
    title = models.CharField(max_length=100, blank=False, default='')
    id = models.CharField(max_length=100, primary_key=True) # TODO: May want to use an auto field (better yet UUIDField) for this imstead (same with author)? https://docs.djangoproject.com/en/4.1/ref/models/fields/#autofield
    origin = models.URLField(blank=False, default='')
    source = models.URLField(blank=False, default=origin)
    description = models.CharField(max_length=500, blank=False, default='')
    contentType = models.CharField(max_length=50, blank=False,
                                                           default='text/plain')
    content = models.TextField(blank=False, default='')    # TODO: This needs to be able to accomodate binary data (base64) as well as text so that images can be stored.
    author = models.ForeignKey(AuthorModel, on_delete=models.CASCADE)   # XXX: Might be better to use set_null or something else, if we want to keep the posts with "deleted user" or something. May be a good idea, consider what might happen to comments on a deleted users post.
    categories = None   # TODO: Figure out how you wanna store a list; with foreign keys or something else, maybe that ArrayField or whatever that needs postgre to work that batu was talking about.
    count = models.PositiveIntegerField(blank=False, default=0)     #TODO: there's probably a way to make this autamatically update and default to the size of the comments table where the post field of the comment is equal to the id of this post
    comments = models.URLField(_(""), max_length=200)   # FIXME: Determine if this is necessary, also, figure out why the snippet pasted in that ("") stuff.
    commentsSrc = None # TODO: This won't actually have a commentssrc field, but a commentssrc model will reference posts with a foreign key.
    published = models.DateTimeField(_(""), auto_now=True, auto_now_add=True)   # FIXME: what's the ("") stuff do?
    visibility = models.CharField(max_length=1, blank=False, default='0', choices=[(PUBLIC, '0'), (FRIENDS, '1')])  #FIXME: Do this better, also use enumeration types: https://docs.djangoproject.com/en/4.1/ref/models/fields/#enumeration-types
    unlisted = models.BooleanField(default=False)
    # TODO: Make sure not missing any fields, nor have unnecessary fields, also do the ordering thing (if it makes sense): Lookup what that Meta thing is in AuthorModel
    
