from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from presentation.models import *

MAX_LENGTH = 200
MIN_LENGTH = 50


class SignUpForm(UserCreationForm):
    displayName = forms.CharField(max_length=MIN_LENGTH, help_text='Required.')
    email = forms.EmailField(
        max_length=MAX_LENGTH, help_text='Required. Inform a valid email address.')
    github = forms.URLField(max_length=MAX_LENGTH,
                            help_text='Required. Infrom a valid Github link.')

    class Meta:
        model = User
        fields = ('username', 'password', 'displayName',
                  'email', 'github')


class AuthorForm(ModelForm):
    username = forms.CharField(
        max_length=150, help_text='Required. 150 characters or fewer. Usernames may contain alphanumeric, _, @, +, . and - characters.')
    password = forms.CharField(help_text='Required.')
    displayName = forms.CharField(max_length=MIN_LENGTH, help_text='Required.')
    email = forms.EmailField(
        max_length=MAX_LENGTH, help_text='Required. Inform a valid email address.')
    github = forms.URLField(max_length=MAX_LENGTH,
                            help_text='Required. Infrom a valid Github link.')

    class Meta:
        model = Author
        fields = ['username', 'password', 'displayName',
                  'email', 'github']
