from django.db import models
from .authorModel import Author
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

# Account username validator
# Validates that the username has not already been taken.
def validateUser(username):
    userAuthor = Author.objects.filter(username=username)
    if(len(userAuthor)!=0):
        raise ValidationError(
            _('Sorry, the username,'+(username)+' has already been taken.'),
        )

# Account Github validator
# Validates that github url link provided is as anticipated.
def validateGithub(github):
    if(github.strip()[0:19] != "https://github.com/"):
        raise ValidationError(
            _(f'This is not a valid GitHub link.'),
        )

# Account Registration Model 
class accountRequest(models.Model):  
    # Account display name
    displayName = models.CharField(blank=True, max_length=100)
    # Account password
    password = models.CharField(max_length=128, verbose_name='password')
    # Account Github
    # Also validates if the github url provided is valid.
    github = models.URLField(validators=[validateGithub], max_length=200, verbose_name='github')
    # Account host url
    host = models.URLField(max_length=200)
    # Account username
    # Also checks if the username is available.
    username = models.CharField(primary_key=True, 
        error_messages={ 'unique': 'This username is not available.'},
        help_text= 'Incorrect input, please try again!', 
        max_length=50, unique=True, validators = [validateUser], verbose_name='username')
