from django.db import models
import uuid
import django.contrib.auth.validators
from api.models.author import Author

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

# Validate if the username is in author table, raise error if in 
# arg   
#       str:username
# return
#       None
def validate_username_nonexist_in_author(the_username):
    # get author with given username
    author_obj = Author.objects.filter(username=the_username)
    if(len(author_obj)!=0):
        raise ValidationError(
            _(f'Username "{the_username}" is already taken.'),
        )
    
    
# model: store sign up requests for admin to accept or decline
class Signup_Request(models.Model):
    
    displayName = models.CharField(blank=True, max_length=150)

    # same fromat requirement as Author
    username    =   models.CharField(primary_key=True, error_messages={'unique': 'The username is already requested by other applier.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True,\
         validators=[validate_username_nonexist_in_author], verbose_name='username')
    
    # password to login 
    password    =   models.CharField(max_length=128, verbose_name='password')

    # Github page
    git_url     =   models.URLField(default='http://github.com/' ,max_length=500)

    # Which host this user was created on
    host        =   models.URLField(max_length=500)
