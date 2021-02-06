from django.db import models
import uuid
# Import Any Related Models
from api.models.author import Author

# The following lists of tuples are used in choices fields to enforce model validation

# List of tuples containing the content-types that are handled by this model
ContentTypes = [
    ('text/markdown'     , 'text/markdown'),
    ('text/plain'        , 'text/plain'),
    ('application/base64', 'application/base64'),
    ('image/png;base64'  , 'image/png;base64'),
    ('image/jpeg;base64' , 'image/jpeg;base64')
]

# Different types of visibilities to the users
VisibilityTypes = [
    ('public' , 'public'),
    ('friends', 'friends')
]

class Post(models.Model):
    # Unique reference to the post itself
    post_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    

    # Because a post can be reshared, we can store the url of the original post
    # This url will store the id of the original post and the original author
    origin_post_url = models.URLField()


    # Who this post was made by
    author_id = models.ForeignKey(Author, on_delete=models.CASCADE)

    # title of the post
    title = models.TextField(max_length=100)

    # description of the post, should be a short summary
    description = models.TextField() # Should a max-length be enforced?

    # This should allow handling of common markdown
    content = models.TextField() 

    # Content type of the posts content, useful for Response
    contentType = models.TextField(null=False, choices=ContentTypes, default='text/plain')

    # Who can view this Post
    visibility = models.CharField(max_length=10, null=False, choices=VisibilityTypes, default='public')
    
    # Not 100% Clear on the usage of this field yet
    unlisted = models.BooleanField(default=False)

    # Date when the model was published
    published = models.DateTimeField(auto_now_add=True)
    
    # Full url of the post
    url = models.URLField()

    # TBD Fields
    # Source, Origin, Categories(maybe use an array field for this??)
